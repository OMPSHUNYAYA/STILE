# ⭐ STILE

## Structural Integration Leverage

### Delivery-State Resolution Without Transport as the Sole Authority

![STILE](https://img.shields.io/badge/STILE-Structural%20Integration%20Leverage-black)
![Version](https://img.shields.io/badge/Version-2.1-blue)
![Profile](https://img.shields.io/badge/Profile-STILE--DELIVERY--ADMISSION--1--D01-purple)
![Python](https://img.shields.io/badge/Python-25%2F25%20PASS-green)
![Browser](https://img.shields.io/badge/Browser-25%2F25%20PASS-green)
![Full Audit](https://img.shields.io/badge/Full%20Audit-30%2F30%20PASS-green)
![Cross Runtime](https://img.shields.io/badge/Cross--Runtime%20Parity-PASS-green)
![Deterministic](https://img.shields.io/badge/Resolution-Deterministic-purple)
![Self Contained](https://img.shields.io/badge/Browser-Self--Contained-orange)

STILE is a bounded deterministic reference model for resolving structural delivery admission while keeping transport observation and consumption observation separate.

The governing relation is:

`structural_delivery_state = resolve(declared_delivery_structure, versioned_rules)`

The core separation is:

`transport_state != structural_delivery_state != consumption_state`

Transport may establish movement.

Structure establishes bounded admissibility.

Consumption may establish use.

None of these lanes is allowed to impersonate the others.

---

## ⚡ Core Guarantee

Within the declared STILE profile:

`same declared structure + same versioned rules -> same structural decision`

The current reference profile is:

`STILE-DELIVERY-ADMISSION-1-D01`

The current schema is:

`2.1.0`

The reference implementation resolves three structural states:

`complete + consistent -> RESOLVED + ADMITTED`

`incomplete -> INCOMPLETE + ABSTAIN`

`conflicting -> CONFLICT + ABSTAIN`

STILE does not force an admission when required structure is missing or conflicting.

---

## 🧱 What STILE Resolves

The current profile evaluates declared structural fields for:

- sender identity;
- receiver identity;
- message identity;
- expected message identity;
- payload identity;
- expected payload identity;
- sender intent;
- receiver expectation;
- context identity;
- explicit conflict state.

The structural decision is separate from:

- transport observations such as `SENT`, `RECEIVED`, or `FAILED`;
- consumption observations such as `UNREAD`, `CONSUMED`, or `REJECTED`.

This allows the structural admission decision to remain stable when later operational observations change.

---

## 🧭 Three Independent Lanes

### Structural Admission

Determines whether the declared delivery structure is complete and consistent.

Possible outcomes:

`RESOLVED + ADMITTED`

`INCOMPLETE + ABSTAIN`

`CONFLICT + ABSTAIN`

### Transport Observation

Records operational movement without rewriting structural admission.

Examples:

`UNKNOWN`

`NOT_OBSERVED`

`SENT`

`RECEIVED`

`FAILED`

### Consumption Observation

Records later use without rewriting structural admission.

Examples:

`UNKNOWN`

`UNREAD`

`CONSUMED`

`REJECTED`

The central invariant is:

`transport-only change -> same structure_hash + same decision_hash + different observation_hash`

`consumption-only change -> same structure_hash + same decision_hash + different observation_hash`

---

## 🔐 Three Evidence Identities

STILE v2.1 produces three SHA-256 identities.

### `structure_hash`

Identifies the declared structural core under the named profile and schema.

Transport and consumption observations are outside this hash.

### `decision_hash`

Identifies:

- the profile;
- the schema;
- the structure hash;
- the resolution;
- the delivery admission;
- the reason codes.

### `observation_hash`

Binds transport and consumption observations to the structural decision without rewriting that decision.

This separation makes it possible to distinguish:

`what was declared`

`what structural decision followed`

`what was later observed`

---

## ⚡ Try STILE v2.1

Run the Python reference:

```text
python reference/stile_delivery_admission_v2_1.py
```

Expected final result:

```text
Conformance: 25/25 PASS
```

Run the Python conformance report only:

```text
python reference/stile_delivery_admission_v2_1.py --self-test
```

Open the browser reference:

[Open the STILE v2.1 Browser Reference](reference/STILE_Delivery_Admission_Browser_Demo_v2_1.html)

The browser reference is self-contained and runs without an API, server-side resolver, external JavaScript library, or external stylesheet.

---

## 🧪 Demonstration Cases

| Case | Resolution | Delivery Admission | Transport | Consumption | Reason |
|---|---|---|---|---|---|
| Aligned | RESOLVED | ADMITTED | NOT_OBSERVED | UNKNOWN | NONE |
| Transport observed | RESOLVED | ADMITTED | RECEIVED | UNKNOWN | NONE |
| Consumed | RESOLVED | ADMITTED | RECEIVED | CONSUMED | NONE |
| Incomplete | INCOMPLETE | ABSTAIN | NOT_OBSERVED | UNKNOWN | MISSING_RECEIVER_ID |
| Identity conflict | CONFLICT | ABSTAIN | NOT_OBSERVED | UNKNOWN | MESSAGE_ID_MISMATCH |
| Payload conflict | CONFLICT | ABSTAIN | NOT_OBSERVED | UNKNOWN | PAYLOAD_HASH_MISMATCH |
| Intent conflict | CONFLICT | ABSTAIN | NOT_OBSERVED | UNKNOWN | INTENT_EXPECTATION_MISMATCH |
| Explicit conflict | CONFLICT | ABSTAIN | NOT_OBSERVED | UNKNOWN | EXPLICIT_CONFLICT |

The first three cases demonstrate that transport and consumption may change while the structural admission decision remains unchanged.

The remaining cases demonstrate explicit refusal to admit incomplete or conflicting structure.

---

## 🔍 What You Will Observe

- deterministic structural resolution;
- explicit separation of admission, transport, and consumption;
- incomplete structure produces `INCOMPLETE + ABSTAIN`;
- conflicting structure produces `CONFLICT + ABSTAIN`;
- repeated evaluation of the same declared structure produces the same structural decision;
- property order does not change the decision;
- transport-only changes do not change the structural decision hash;
- consumption-only changes do not change the structural decision hash;
- Python and browser reference implementations agree on baseline and Unicode hash fixtures;
- unsupported observation values are surfaced explicitly as `INVALID`.

---

## 🔥 Break This STILE

The current profile should be considered broken if any of the following can be demonstrated within the declared model:

`same declared structure + same versioned rules -> different structural decision`

`same declared structure + same versioned rules -> different decision_hash`

`transport-only change -> different structure_hash`

`transport-only change -> different decision_hash`

`consumption-only change -> different structure_hash`

`consumption-only change -> different decision_hash`

`incomplete structure -> ADMITTED`

`conflicting structure -> ADMITTED`

`same canonical fixture -> different Python and browser hashes`

The verification package is designed to test these conditions directly.

---

## 🛡 Structural Safety Model

STILE does not force a positive decision when its declared structural requirements are not satisfied.

`incomplete -> INCOMPLETE + ABSTAIN`

`conflicting -> CONFLICT + ABSTAIN`

`complete + consistent -> RESOLVED + ADMITTED`

This is a bounded admission model.

It is not a claim that every real-world delivery question can be reduced to these fields.

---

## 🌐 Truth, Movement, and Use

STILE separates three questions that are often collapsed into one.

### Did the data move?

That belongs to transport observation.

### Is the declared delivery structure admissible under the current profile?

That belongs to structural admission.

### Was the content read, consumed, rejected, or otherwise used?

That belongs to consumption observation.

The current model therefore does not use physical transmission as the sole authority over structural admission.

It also does not use later consumption as the sole authority over structural admission.

---

## ⚠️ Claim Boundary

STILE v2.1 demonstrates a bounded deterministic structural admission model.

It does not claim that:

- physical transmission is unnecessary for systems that must physically transmit data;
- structural admission proves that bytes reached a remote endpoint;
- structural admission proves that a recipient read, consumed, or acted on content;
- messaging protocols, networks, acknowledgements, retries, queues, or transport systems are universally unnecessary;
- the current profile is a universal delivery oracle.

The reference claim is narrower:

`transport observation is not the sole authority over the bounded structural admission decision`

and:

`consumption observation is not the sole authority over the bounded structural admission decision`

Within the declared profile:

`same declared structure + same versioned rules -> same structural decision`

---

## 📊 Resolution Summary

| Structural Condition | Resolution | Delivery Admission |
|---|---|---|
| Complete and consistent | RESOLVED | ADMITTED |
| Incomplete | INCOMPLETE | ABSTAIN |
| Conflicting | CONFLICT | ABSTAIN |

Transport and consumption observations remain independent of this structural classification.

---

## 🔁 Deterministic Properties

The current reference implementation verifies:

`same structure -> same decision`

`same canonical content in different key order -> same decision`

`transport-only change -> same structural decision`

`consumption-only change -> same structural decision`

`structural change -> structurally bound hashes may change`

The model is version-bound:

`profile + schema + declared structure -> structure_hash`

A schema change therefore intentionally changes the associated evidence identity.

---

## 🌍 Practical Interpretation

STILE can sit alongside existing transport and messaging systems.

A transport system may record movement.

A receiving system may record consumption.

STILE resolves a separate question:

`is the declared delivery structure admissible under the named profile and versioned rules?`

This separation can be useful wherever systems need deterministic admission decisions without allowing one operational signal to become the sole authority over the entire state.

Potential areas of exploration include:

- APIs and service integration;
- offline-first workflows;
- distributed record exchange;
- financial coordination;
- disaster-response information systems;
- healthcare data workflows;
- IoT state exchange;
- multi-party structural admission.

These are application directions, not claims that the current reference profile already solves every domain-specific requirement.

---

## ✅ Verification Status

STILE v2.1 has the following reference verification results:

`Python conformance -> 25/25 PASS`

`Browser built-in conformance -> 25/25 PASS`

`Full browser audit -> 30/30 PASS`

`Visible demonstration cases -> 8/8 expected`

`Baseline cross-runtime hash parity -> PASS`

`Unicode cross-runtime hash parity -> PASS`

`Invalid observation handling parity -> PASS`

For complete verification steps and expected hashes:

[Read the STILE v2.1 Verification Guide](VERIFY/VERIFY.md)

For the frozen SHA-256 identities of the reference files:

[View the STILE v2.1 SHA-256 Freeze](VERIFY/FREEZE_DEMO_SHA256.txt)

---

## 🔗 Active Reference Files

- [STILE v2.1 Python Reference](reference/stile_delivery_admission_v2_1.py)
- [STILE v2.1 Browser Reference](reference/STILE_Delivery_Admission_Browser_Demo_v2_1.html)
- [STILE v2.1 Verification Guide](VERIFY/VERIFY.md)
- [STILE v2.1 SHA-256 Freeze](VERIFY/FREEZE_DEMO_SHA256.txt)

---

## 🧭 Framework Context

STILE is developed within the Shunyaya Framework.

Its current contribution is a specific structural separation:

`transport establishes movement`

`structure establishes admissibility`

`consumption establishes use`

The purpose is not to erase transport, networking, or execution.

The purpose is to prevent those operational mechanisms from automatically becoming the sole authority over a bounded structural admission decision.

---

## 🔗 Related Structural References

- [ORL](https://github.com/OMPSHUNYAYA/Orderless-Ledger) — deterministic ledger classification without arrival order or clock metadata as decision authority
- [STOCRS](https://github.com/OMPSHUNYAYA/STOCRS) — structural computation research
- [STIME](https://github.com/OMPSHUNYAYA/Structural-Time) — structural progression without physical clocks as the sole time authority
- [SSUM-Time](https://github.com/OMPSHUNYAYA/SSUM-Time) — structural time reconstruction and recovery
- [STRAL-Path](https://github.com/OMPSHUNYAYA/STRAL-Path) — structural path research
- [SLANG-Computation](https://github.com/OMPSHUNYAYA/SLANG-Computation) — structural computation and resolution
- [STINT-Money](https://github.com/OMPSHUNYAYA/STINT-Money) — structural settlement-state research

---

## 📜 **License**

See: [LICENSE](LICENSE)

The repository is a publicly available reference implementation under its stated license terms.

Architecture documentation is subject to the licensing terms declared in the repository, including CC BY-NC 4.0 where stated.

The repository does not claim recognition as a formal technical standard.

---

### Final Statement

A transport event and a structural admission decision are not the same thing.

A consumption event and a structural admission decision are not the same thing.

STILE v2.1 keeps these states separate and resolves structural admission deterministically under a declared profile and schema.

`transport establishes movement`

`structure establishes admissibility`

`consumption establishes use`
