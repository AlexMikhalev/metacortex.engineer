---
title: "The Domain Model as Quality Thread: How JSON Schema Survives From Whiteboard to Production"
subtitle: "Eighteen data artefacts, five ZDP gates, one canonical domain model. The only known way to carry quality through the full software lifecycle."
slug: "domain-model-quality-thread"
description: "How a single JSON Schema-validated domain model carries quality from inception through to production operations, with 18 artefacts and 5 gate reviews."
tags: ["domain-model", "quality", "architecture", "JSON-Schema", "software-lifecycle"]
author: "Dr Alexander Mikhalev"
date: "2026-04-17"
draft: false
---

Eighteen data artefacts, five ZDP gates, one canonical domain model. The only known way to carry quality through the full software lifecycle.

---

## The Quality Gap Problem

Here is a pattern I have seen repeat across every organisation I have worked with, from three-person startups to consultancies delivering for FTSE 100 clients. The quality is excellent at the beginning of a project. The requirements are sharp. The domain language is precise. The team can explain every entity and relationship in the system.

Then implementation begins, and something breaks.

It is not a single catastrophic failure. It is a slow degradation. The term "borrower" in the domain model becomes "customer" in the API, then "user" in the frontend, then "applicant" in the database. A state machine defined with ten states and fourteen transitions gets compressed to four states because the backend developer did not see the point of "Blocked - Dependency Outage" as distinct from "Blocked - Conditions Outstanding". The activation checklist, which domain experts described with eleven specific items and evidence requirements, becomes a generic "checklist" table with a JSON blob.

By the time the system reaches production, the connection between what the business asked for and what was built is threadbare. Operations teams invent their own terminology. Incident responders cannot trace a failure back to the original domain concept. And nobody can answer the simplest question from a new team member: "What does this system actually do?"

I have been that person unable to answer. I have also been the person who let it happen.

The root cause is always the same: **there is no continuous thread that carries domain truth from inception through to production operations**. Each phase of the lifecycle creates its own artefacts in its own language, and the translation between phases is lossy. Whiteboard to Jira ticket loses nuance. Jira ticket to code loses context. Code to database schema loses intent. Database to monitoring loses semantics entirely.

This is not a tooling problem. It is a structural problem. And the solution is not better tools or more meetings. It is a single, versioned, machine-readable domain model that every subsequent artefact traces back to.

---

## The Domain Model as Single Source of Truth

A domain model in this context is not a UML diagram on a wall. It is not a Confluence page with a table of definitions. It is a JSON Schema-validated document that lives in the repository, is versioned alongside the code, and is referenced by every downstream artefact in the pipeline.

Here is what a real one looks like, taken from a client project we delivered for a loan management platform:

```json
{
  "version": "1.0",
  "title": "Charm Loan Management Platform",
  "project_type": "client",
  "project_slug": "charm",
  "lifecycle": {
    "state": "draft"
  },
  "scope": {
    "covers": [
      "Loan application lifecycle from eligibility through activation",
      "Borrower portal multi-step form orchestration",
      "Audit trail immutability and compliance traceability"
    ],
    "excludes": [
      "Content authoring for legal document templates",
      "Zoho CRM internal configuration and customisation"
    ],
    "boundary_rationale": [
      {
        "boundary": "No legal document authoring",
        "rationale": "System handles preparation, versioning, storage, and execution evidence only; authoring is upstream"
      }
    ]
  },
  "terms": {
    "loan_activation_record": {
      "label": "Loan Activation Record",
      "definition": "Authoritative record tracking a loan from IC approval through gated readiness, Portfolio Officer authorisation, and forward-only transition to Active.",
      "synonyms": ["activation record", "LAR"],
      "category": "orchestration",
      "lifecycle_stages": [
        "In Progress",
        "Blocked - Conditions Outstanding",
        "Blocked - Dependency Outage",
        "Paused - Borrower Deadline",
        "Completed",
        "Active",
        "Activated In Error - Contained",
        "Activated In Error - Corrected",
        "Cancelled Pre-Activation",
        "Expired/Lapsed Approval"
      ],
      "avoid": [
        {
          "term": "loan application",
          "reason": "Loan Application covers the broader intake; Activation Record specifically tracks the post-IC-approval activation lifecycle"
        }
      ]
    }
  }
}
```

Several things are worth noting about this structure.

First, the `avoid` field. This is not decoration. The distinction between "Loan Application" and "Loan Activation Record" is the kind of thing that causes real bugs when conflated. We have seen production incidents where a developer treated "application rejected" and "activation expired" as the same state transition. They are not. The domain model makes this explicit and machine-enforceable.

Second, the `lifecycle_stages` array. Ten states, not four. The reason "Blocked - Dependency Outage" exists as a separate state from "Blocked - Conditions Outstanding" is that the remediation paths are completely different. A dependency outage requires waiting for an external system to recover. A conditions outstanding state requires human intervention by a Portfolio Officer. Collapsing these into a single "Blocked" state would destroy the operational semantics that the business relies on for SLA tracking and escalation.

Third, the `scope.excludes` with `boundary_rationale`. This prevents scope creep in the most direct way possible: by making exclusions first-class citizens with explicit reasoning. When a stakeholder asks "can we also handle document authoring?", the answer is already documented with rationale.

The schema itself is JSON Schema Draft 2020-12, stored in the repository alongside the code. The lifecycle state field maps directly to the ZDP gate milestones. `draft` means the model exists but has not passed its Lifecycle Objectives review. `baselined` means it has been walked through with domain experts and signed off. `locked` means the architecture review has confirmed that solution design artefacts trace back correctly. And so on through to `released`, which means the system is in production and the domain model has survived the full journey.

---

## The 18-Artefact Pipeline

The domain model is the first artefact, but it does not travel alone. It is the first of eighteen data artefacts that flow through what we call the ZDP lifecycle -- six stages from Discovery through to Drive, with a gate review at each transition.

**Phase 1: Domain Inception (Artefacts 1-4)**

Artefact 1 is the Atomic Domain Model -- the JSON document shown above. Artefact 2 is a set of End-to-End Business Scenarios: complete workflows from trigger to outcome, crossing organisational boundaries, with happy paths and exception paths. Artefact 3 is a Journey Map annotated with data touchpoints: what data is created, consumed, transformed, or deleted at each step. Artefact 4 is a Business Events Model: domain events that signal state transitions, each referencing the domain model entities it affects.

The critical thing about Phase 1 is that nothing here is about solution design. We are still in the problem space.

We learnt this the hard way on a loan activation project. We skipped Artefact 4 (the Business Events Model) on the first iteration and went straight from domain model to API design. The result was a system where the "loan activated" event was published before the audit trail entry was written -- a temporal ordering violation that caused a real production incident.

**Phase 2: Solution Design (Artefacts 5-7)**

Artefact 5 is a Baselined Process Model (BPMN or equivalent), validated against all business scenarios. Artefact 6 is a Data Schema: logical and physical data models derived from the domain model. Artefact 7 is API Specifications (OpenAPI/AsyncAPI) defining data contracts between components.

Each of these traces back to Phase 1 artefacts. Every API endpoint references a business event. Every data schema entity references a domain model term. If an entity appears in the data schema that does not trace back to the domain model, it either needs to be added to the domain model (with justification) or removed from the schema.

**Phase 3: Implementation (Artefacts 8-14)**

Seven artefacts: Use Case Data Structures (TypeScript/Rust types derived from API specs), Responsible AI and Accessibility Governance, Data and Model Specifications, Pipeline Specifications (ETL with lineage tracking), Synthetic Data Sets (privacy-preserving test data), Prompt and Agent Specifications (for systems involving LLMs), and a Lifecycle Register tracking every model and prompt version.

**Phase 4: Operations (Artefacts 15-18)**

Ops Runbook (data incident procedures, schema migration protocols), Performance and Drift Report, AI Incident and Escalation Report, and the System Knowledge Base -- a living glossary of all domain terms and canonical definitions.

The last artefact closes the loop. Artefact 18 feeds back into Artefact 1. Production learning refines domain definitions. The pipeline is not linear. It is a cycle.

---

## Gate Verification: Where Quality Is Checked

Having eighteen artefacts is meaningless if nobody checks whether they are correct. Each ZDP gate enforces a verification step:

| Gate | Artefacts Verified | Method |
|------|-------------------|--------|
| LCO (Lifecycle Objectives) | 1-4 | Domain expert walkthrough, scenario coverage analysis |
| LCA (Lifecycle Assessment) | 5-7 | Architecture review, contract compatibility testing, traceability audit |
| IOC (Initial Operational Capability) | 8-14 | Code review, synthetic data validation, responsible AI audit |
| FOC (Full Operational Capability) | 15 | Runbook dry-run, incident simulation |
| CLR (Continuous Learning Release) | 16-18 | Drift detection validation, glossary accuracy review |

The LCA gate is the most important in practice. This is where we run a traceability audit: every element in the Data Schema (Artefact 6) must trace back to at least one element in the Domain Model (Artefact 1). Every API endpoint (Artefact 7) must reference a Business Event (Artefact 4).

We do this audit mechanically. The domain model is JSON. The data schema is derivable from the code. The API specs are OpenAPI. We can write scripts that check traceability rather than relying on manual review. When a field appears in the database that does not map to a domain model term, the build fails.

This is the part that surprises people. They expect gate reviews to be meetings. They are not. They are automated checks with human judgement at the boundaries.

---

## What This Looks Like in Practice

On the Charm loan management platform, the domain model defined 26 core entities across 9 bounded contexts. The model included a complete state machine for the loan activation lifecycle with 10 states and 14 transitions. It specified `active_is_immutable = true` as a core invariant: once a loan reaches the Active state, there is no rollback. Corrections happen through new records, never through mutation.

This single design decision -- immutable activation -- rippled through every subsequent artefact. The API specifications could not include a PATCH endpoint for activation records. The database schema required an append-only audit trail table. The ops runbook needed a specific procedure for "activated in error" scenarios.

Without the domain model making this explicit at Phase 1, we would have discovered the requirement at Phase 3 (or worse, Phase 4) when a developer asked "can we just update the activation record status back to In Progress?" The answer was no. The domain model said so. And because it said so at the beginning, every downstream artefact was designed with that constraint from the start.

---

## Why Most Organisations Skip This

The honest answer is that most organisations skip this because it feels slow. Writing a domain model before writing code feels like documentation, and documentation feels like overhead.

What I have learnt from building systems both ways -- with and without the domain model thread -- is that the upfront investment pays for itself somewhere between Phase 2 and Phase 3 of every project. The projects without a domain model spend those phases in endless clarification meetings, resolving ambiguities that should have been settled at inception. The projects with a domain model spend those phases implementing.

The cost of not doing this compounds. A domain model that takes two weeks to write at Phase 1 saves maybe one week at Phase 2. But it saves three weeks at Phase 3, because every implementation decision references the canonical definitions rather than someone's recollection of a meeting from two months ago. And it saves something harder to measure at Phase 4: the ability to diagnose production incidents by tracing a failure back through the artefact chain to the original domain concept.

The approach I have described is not theoretical. It is the data spine of the Zestic AI Development Process, which we have applied across multiple client engagements. The 18-artefact pipeline, the gate verification, the feedback loops -- these are operational patterns, not aspirational ones.

The domain model is not the most exciting part of software development. But it is, I have become convinced, the single most effective mechanism for carrying quality from the whiteboard to production and back again. If you do not have a machine-readable, versioned, traceable domain model at the centre of your development process, you are hoping that quality survives the journey. Hope is not a strategy.
