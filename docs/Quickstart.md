# ⭐ STILE — Quickstart

## Structural Integration Leverage

### Delivery-State Resolution Without Transport as the Sole Authority

**Deterministic • Structure-Based • Bounded Structural Admission**

STILE v2.1 separates:

`transport movement`

`structural admissibility`

`consumption`

The core relation is:

`transport_state != structural_delivery_state != consumption_state`

The governing resolution rule is:

`structural_delivery_state = resolve(declared_delivery_structure, versioned_rules)`

Within the declared profile:

`same declared structure + same versioned rules -> same structural decision`

---

## ⚡ 30-Second Start

From the repository root, run:

```bash
python reference/stile_delivery_admission_v2_1.py
```

Expected final result:

```text
Conformance: 25/25 PASS
```

The Python reference also prints eight demonstration cases covering:

`RESOLVED + ADMITTED`

`INCOMPLETE + ABSTAIN`

`CONFLICT + ABSTAIN`

---

## 🧪 Run the Python Conformance Report

```bash
python reference/stile_delivery_admission_v2_1.py --self-test
```

Expected report values:

`status = PASS`

`passed = 25`

`total = 25`

---

## 🌐 Open the Browser Reference

Open:

`reference/STILE_Delivery_Admission_Browser_Demo_v2_1.html`

directly in a modern browser.

The browser reference is self-contained and does not require:

- an API;
- a server-side resolver;
- an external JavaScript library;
- an external stylesheet.

The built-in browser conformance result should be:

`25/25 PASS`

For the broader `30/30` browser audit, follow:

`VERIFY/VERIFY.md`

---

## 🔍 What to Observe

The reference demonstrates that the structural admission decision is separate from transport and consumption observations.

### Structural admission

`complete + consistent -> RESOLVED + ADMITTED`

`incomplete -> INCOMPLETE + ABSTAIN`

`conflicting -> CONFLICT + ABSTAIN`

### Transport observation

Examples:

`UNKNOWN`

`NOT_OBSERVED`

`SENT`

`RECEIVED`

`FAILED`

### Consumption observation

Examples:

`UNKNOWN`

`UNREAD`

`CONSUMED`

`REJECTED`

The key lane-separation behavior is:

`transport-only change -> same structure_hash + same decision_hash + different observation_hash`

`consumption-only change -> same structure_hash + same decision_hash + different observation_hash`

---

## 🧱 Current Structural Core

The current reference profile evaluates:

`sender_id`

`receiver_id`

`sender_message_id`

`receiver_expected_message_id`

`sender_payload_hash`

`receiver_expected_payload_hash`

`sender_intent`

`receiver_expectation`

`context_id`

`conflict`

The two observation fields are separate from this structural core:

`transport_observation`

`consumption_observation`

---

## 🔬 Resolution Model

The active profile is:

`STILE-DELIVERY-ADMISSION-1-D01`

The active schema is:

`2.1.0`

The resolver follows three mutually exclusive branches:

`not complete -> INCOMPLETE + ABSTAIN`

`complete AND not consistent -> CONFLICT + ABSTAIN`

`complete AND consistent -> RESOLVED + ADMITTED`

This is a bounded structural admission model.

---

## 🔐 Evidence Identities

STILE v2.1 produces three SHA-256 identities.

### Structure Hash

`structure_hash`

Identifies:

`profile + schema + structural core`

Transport and consumption observations are outside this hash.

### Decision Hash

`decision_hash`

Identifies:

`profile + schema + structure_hash + resolution + delivery_admission + reason_codes`

### Observation Hash

`observation_hash`

Identifies:

`decision_hash + transport_observation + consumption_observation`

This allows observations to change without rewriting the structural decision identity.

---

## 🔁 Determinism Check

Run the Python reference more than once:

```bash
python reference/stile_delivery_admission_v2_1.py
```

For the same declared input under the same versioned rules, expect the same:

`resolution`

`delivery_admission`

`reason_codes`

`structure_hash`

`decision_hash`

`observation_hash`

The core guarantee is:

`same declared structure + same versioned rules -> same structural decision`

---

## 🧭 Three-Lane Interpretation

### Transport establishes movement

Transport may be operationally necessary when data must physically move.

### Structure establishes admissibility

STILE resolves whether the declared structure is admissible under the active profile and schema.

### Consumption establishes use

Consumption records later reading, acceptance, rejection, or use.

These are distinct states.

---

## ⚠️ What STILE Does Not Claim

STILE v2.1 does not claim that:

- physical transmission is unnecessary where data must move;
- structural admission proves remote receipt;
- structural admission proves human reading or consumption;
- networking is universally unnecessary;
- acknowledgements or retries are universally unnecessary;
- the current profile is a universal delivery oracle;
- deterministic resolution guarantees factual truth;
- the model provides consensus, finality, or legal delivery.

The bounded claim is:

`transport observation is not the sole authority over the bounded structural admission decision`

and:

`consumption observation is not the sole authority over the bounded structural admission decision`

---

## ✅ Current Verification Status

The current reference pair has been verified with:

`Python conformance -> 25/25 PASS`

`Browser built-in conformance -> 25/25 PASS`

`Full browser audit -> 30/30 PASS`

`Visible demonstration cases -> 8/8 expected`

`Baseline cross-runtime hash parity -> PASS`

`Unicode cross-runtime hash parity -> PASS`

`Invalid observation handling parity -> PASS`

For the complete verification procedure, use:

`VERIFY/VERIFY.md`

For the frozen SHA-256 file identities, use:

`VERIFY/FREEZE_DEMO_SHA256.txt`

---

## 📁 Repository Structure

```text
STILE/
├── README.md
├── LICENSE
│
├── reference/
│   ├── STILE_Delivery_Admission_Browser_Demo_v2_1.html
│   └── stile_delivery_admission_v2_1.py
│
├── docs/
│   ├── FAQ.md
│   ├── Proof-Sketch.md
│   ├── Quickstart.md
│   ├── STILE-Architecture-Notes.md
│   ├── STILE-Message-Delivery.png
│   ├── Dependency-Elimination-Framework.png
│   └── Shunyaya-Structural-Stack.png
│
└── VERIFY/
    ├── VERIFY.md
    └── FREEZE_DEMO_SHA256.txt
```

---

## 🖼 Documentation Map

For the current STILE model:

`README.md`

For common questions and boundaries:

`docs/FAQ.md`

For the bounded deterministic argument:

`docs/Proof-Sketch.md`

For architectural detail:

`docs/STILE-Architecture-Notes.md`

For the main STILE visual:

`docs/STILE-Message-Delivery.png`

For broader Shunyaya context:

`docs/Dependency-Elimination-Framework.png`

`docs/Shunyaya-Structural-Stack.png`

For verification and exact file identities:

`VERIFY/VERIFY.md`

`VERIFY/FREEZE_DEMO_SHA256.txt`

---

## ⭐ One-Line Summary

STILE v2.1 deterministically resolves whether declared delivery structure is admissible under a named profile and schema, while keeping transport movement and later consumption as separate observations rather than treating either as the sole authority over the structural decision.
