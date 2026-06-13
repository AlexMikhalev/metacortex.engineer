---
title: "Rust Binary Optimisation for Minimal Docker Images"
subtitle: "How to shrink Rust Docker images from 1.2GB to 14MB using musl static linking, LTO, and scratch containers."
slug: "rust-binary-optimisation-docker"
description: "Practical guide to optimising Rust binaries for Docker: musl static linking, link-time optimisation, codegen-units, and scratch containers for sub-15MB images."
tags: ["rust", "docker", "optimisation", "devops"]
author: "Dr Alexander Mikhalev"
date: "2026-05-09"
draft: false
---

Rust produces fast binaries, but the default Docker images are enormous. A typical Rust API server compiled with the standard `rust:latest` base image weighs in at over 1.2GB. That is wasteful for deployment, slow to pull, and expensive to store at scale.

Here is how to get that image down to 14MB -- with no loss of functionality.

## The Problem

A standard Rust Dockerfile looks like this:

```dockerfile
FROM rust:latest
WORKDIR /app
COPY . .
RUN cargo build --release
CMD ["./target/release/myapp"]
```

This produces an image over 1.2GB because it includes the entire Rust toolchain, system libraries, and build artefacts. None of that is needed at runtime.

## The Solution: Static musl + Scratch

### Step 1: Cargo Profile for Size

Add to your `Cargo.toml`:

```toml
[profile.release]
opt-level = 's'       # Optimise for size
lto = true            # Link Time Optimisation
codegen-units = 1     # Maximum size reduction
panic = 'abort'       # Removes unwinding code
```

Each flag does something specific:

- **`opt-level = 's'`** tells the compiler to optimise for binary size instead of speed. For most API servers, the difference is negligible.
- **`lto = true`** performs optimisation across all crates at link time, eliminating dead code that crosses crate boundaries.
- **`codegen-units = 1`** forces the compiler to use a single codegen unit, allowing more aggressive optimisation at the cost of compile time.
- **`panic = 'abort'`** removes the stack unwinding machinery, saving ~200KB.

### Step 2: Multi-Stage Dockerfile with musl

```dockerfile
FROM rust:latest AS builder

RUN rustup target add x86_64-unknown-linux-musl
RUN apt update && apt install -y musl-tools musl-dev
RUN update-ca-certificates

WORKDIR /app
COPY . .
RUN cargo build --release --bin myapp \
    --target x86_64-unknown-linux-musl
RUN strip -s /app/target/x86_64-unknown-linux-musl/release/myapp

FROM scratch AS runtime
COPY --from=builder \
    /app/target/x86_64-unknown-linux-musl/release/myapp \
    /myapp
ENV PORT=80
EXPOSE 80
ENTRYPOINT ["/myapp"]
```

### Step 3: What Each Piece Does

**musl static linking**: Compiling against musl libc instead of glibc produces a fully static binary with zero dynamic dependencies. No `libc.so`, no `libgcc`, nothing.

**`strip -s`**: Removes debug symbols and symbol tables. This alone saves 5-15MB depending on binary size.

**`FROM scratch`**: The final image contains literally nothing except your binary. No shell, no package manager, no libraries. The smallest possible container.

## Results

| Configuration | Image Size | Notes |
|--------------|-----------|-------|
| Standard `rust:latest` | ~1.2GB | Everything included |
| Multi-stage with glibc | ~80MB | Debian slim base |
| Multi-stage with musl + scratch | **~14MB** | Static binary only |

That is an 85x reduction.

## Earthly Alternative

If you use Earthly instead of Docker directly:

```earthfile
VERSION 0.7

build:
    FROM rust:latest
    RUN rustup target add x86_64-unknown-linux-musl
    RUN apt update && apt install -y musl-tools musl-dev
    RUN update-ca-certificates
    WORKDIR /app
    COPY --dir src Cargo.lock Cargo.toml .
    RUN cargo build --release --bin myapp \
        --target x86_64-unknown-linux-musl
    RUN strip -s /app/target/x86_64-unknown-linux-musl/release/myapp
    SAVE ARTIFACT /app/target/x86_64-unknown-linux-musl/release/myapp

docker:
    FROM scratch
    COPY --chmod=0755 +build/myapp /myapp
    ENV PORT=80
    EXPOSE 80
    ENTRYPOINT ["/myapp"]
    SAVE IMAGE myapp:latest
```

## Considerations

### SSL/TLS

Static musl binaries cannot use the system's OpenSSL. Use `rustls` instead of `openssl-sys` in your `Cargo.toml`:

```toml
[dependencies]
reqwest = { version = "0.12", features = ["rustls-tls"], default-features = false }
```

### DNS Resolution

musl's DNS resolver reads `/etc/resolv.conf`. If your binary needs DNS, copy it into the scratch image:

```dockerfile
COPY --from=builder /etc/resolv.conf /etc/resolv.conf
```

Or better: use a minimal base like `alpine` (5MB) instead of `scratch` if you need DNS.

### CA Certificates

For HTTPS from a scratch image:

```dockerfile
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
```

## Why This Matters for AI Infrastructure

Small images are not just about storage costs. They affect deployment speed, cold start times, and security surface area.

For [AI Dark Factory](/post/deploying-ai-dark-factory/) deployments, where containers spin up and down frequently, a 14MB image pulls in under a second versus 30+ seconds for a 1.2GB image. That is the difference between a responsive CI pipeline and one where developers switch context while waiting.

---

*Terraphim AI uses these techniques across all Rust services. [Learn more](https://terraphim.ai).*
