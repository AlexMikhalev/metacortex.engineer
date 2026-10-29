---
title: "Bit-Exact Rust-to-Goose Ports: ahash, fxhash, Aho-Corasick and a B+ Tree"
subtitle: "Three reusable packages for Terraphim's search substrate in Goose, verified against the crates' own test corpora — 340 AC cases, 5900 BTreeMap ops, 124 hash vectors, zero divergence."
slug: "goose-substrate-packages-bitexact-rust-port"
description: "How we ported ahash, fxhash, Aho-Corasick and BTreeMap semantics from Rust to Goose with a reference harness that emits golden vectors straight from the real crates."
tags: ["goose", "rust", "terraphim", "porting", "verification", "aho-corasick"]
author: "Dr Alexander Mikhalev"
date: "2026-10-29"
draft: false
---

Shipped: three reusable packages for Terraphim's search and agent substrate, written in Goose — the compiled language from the author of FlatBuffers — and verified not against hand-written expectations but against the Rust crates' own test suites.

- `libs/ahashmap` — `ahash` 0.8.12 + `rustc-hash` 2.1.3, bit-exact (124/124 vectors)
- `libs/ahocorasick` — `aho-corasick` 1.1.3 semantics, 340/340 corpus cases
- `libs/bbtree` — ordered map over a B+ tree, 5900/5900 ops vs `std::BTreeMap`

All merged to `flashmap-goose` on `task/19-substrate-packages`, PR #20.

## Why Goose

We already run `flashmap-goose`: a Goose port of the FlashMap speculative-decoding substrate, with 25+39 golden checks green. Terraphim's grep and agent components need the same treatment, but they sit on three crates with *exact* semantics — you can't hand-wave "mostly the same":

- `aho-corasick` — the match engine behind thesaurus-driven search
- `ahash` / `rustc-hash` — the table hashing used across rolegraphs, embeddings and command tables
- `BTreeMap` — deterministic sorted serialisation in manifests and command dedup

## The Discipline: Crate Corpus, Not Assertions

Rather than writing tests from our reading of the semantics, we built a small Rust harness that runs the *real* crates and emits TSV golden vectors:

- `ac_cases.tsv` — the crate's own `SearchTest` tables, verbatim: 457 rows covering Standard, LeftmostFirst, LeftmostLongest, overlapping, anchored and ASCII case-insensitive semantics
- `hash_vectors.tsv` — ahash through `RandomState::with_seeds(0,0,0,0)` plus FxHasher, across u64/bytes/str inputs
- `btree_ops.tsv` — a 5900-op deterministic log run through `std::BTreeMap`

The Goose tests then replay the TSVs and compare exactly. The oracle is the crate itself — if our understanding of "Standard semantics" was wrong, the corpus says so by name.

## What the Corpus Taught Us

The interesting part is what we got *wrong* initially:

**Standard ≠ leftmost-first.** Aho-Corasick's Standard match semantics commit the *earliest-ending* match, not the longest or earliest-inserted. `standard030` (`["abcd","abc","ab"]` on `"abcd"`) proves it: `(2,0,2)` — the shortest wins at a shared start.

**Zero-width patterns have adjacency rules.** Empty patterns match at every position, but a zero-width hit is suppressed when it sits exactly on the end of a committed real match — and after a zero-width commit, the next match must start strictly past it. `leftfirst010` (`["","a"]` on `"a"` → `(0,0,0),(0,1,1)`) pins the rule: the empty pattern wins position 0, suppresses `"a"`, then matches again at position 1.

**Yield order matters.** The overlapping iterator emits real outputs before zero-width hits at the same end position (`over320`–`over340` prove it by pattern index).

None of this is obvious from a casual read of the algorithm. It's all in the tables, and the tables are now regression armour.

## Numbers

**Compile time**: clean `cargo build --release` of the reference bench ≈ **2.9 s**;
`goose check` on each bench ≈ **12 ms** — one reason the iteration loop on
the Goose side is pleasant.

**Run time**, identical workloads both sides (same LCG streams — outputs
match bit-for-bit):

| metric | Rust | Goose | ratio |
|---|---|---|---|
| AC scan, 10×1MiB | 41ms | 196ms | 4.8x |
| B+ insert 200k | 19ms | 89ms | 4.7x |
| B+ ordered walk | 0.4ms | 0.7ms | 1.7x |
| ahash 1M keys | 3.2ms | 128ms | 39x |

The hash gap is honest: Goose lacks unaligned 128-bit reads, so `le64` is a byte loop. Reason-then-measure follow-up. The data-structure ratios are where the port actually lives.

## The Optimisation Arc: Closing the Gap

We then ran that follow-up properly — a full optimisation harness: crate-oracle fuzz corpora, property testing, an evolutionary variant sweeper, and a native `extern fn` tier. The arc:

![The optimisation arc](/post/img/goose-arc.svg)

| metric | baseline | optimised | Rust | ratio now |
|---|---|---|---|---|
| ahash 1M keys | 128ms | **2.04ms** | 3.2ms | **0.64x — faster than Rust** |
| fxhash 1M | 110ms | **1.05ms** | 1.1ms | **0.95x — parity** |
| AC scan 10x1MiB | 196ms | **52.9ms** | 44ms | **1.2x — near parity** |
| btree get (batch lanes) | 89ms | **17.6ms** | 16ms | **1.1x — parity** |

**How** — the layers that measured, in order:

1. **`gs_ld64` gather shape** — the codegen folds the `s[i..i+8]` + byte-OR pattern into memcpy unaligned loads; the `for` loop form it didn't
2. **`extern fn` + `c_sources`** — package-native C for `__uint128_t` folded multiply and whole hot loops; no compiler fork needed
3. **Batch APIs** — one call per million keys instead of one per key: the ABI amortisation was the biggest single win (hash 10x → parity)
4. **Byte-class packed DFA** — the aho-corasick crate's own dense-DFA shape: 256-wide transitions folded to ~30 equivalence classes (8x smaller table, better cache residency)
5. **Batch lanes** — 16 interleaved btree descents so the memory system overlaps the per-level dependent loads

**Verified, triple-oracle** — every optimisation is gated by the same corpora plus a fuzz layer: 8,298 hash vectors from the real crates (incl. regex 1.13.1 testdata mined), 51 random AC cases, 35,000 btree ops across `std::BTreeMap` *and* a Python oracle, and self-oracle property tests (native ≡ pure on every random input). Sinks stay bit-identical.

![Verification pipeline](/post/img/goose-verify.svg)

The evolutionary sweeper (`bench/evolve.py`) earned its keep on day one: it found FAN=16 optimal for the flat-blob btree (smaller nodes beat scan-width on this workload) — applied and measured, not guessed. Things tried and *reverted* after measuring: binary search inside nodes, special-state flags, `ocnt` gating — all slower here, all documented.

## Dedup, and What's Next

The port killed three duplicated copies of the automaton and thesaurus modules — `tgrep`, `agent`, and `thesaurus/` (now a package) all consume `libs/`. The next step is swapping the remaining bespoke structures in `terraphim-grep`'s Goose port onto these packages, then the agent command tables onto `ahashmap` + `bbtree`.

Full detail: [flashmap-goose PR #20](https://git.terraphim.cloud/terraphim/flashmap-goose/pulls/20) — research, design, KLS reviews and per-step commits under `Refs #19`.
