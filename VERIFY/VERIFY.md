# STILE v2.1 Verification Guide

## Structural Integration Leverage

STILE v2.1 separates structural delivery admission from transport observation and consumption observation.

The bounded reference model verifies:

`transport_state != structural_delivery_state != consumption_state`

and:

`same declared structure + same versioned rules -> same structural decision`

Transport may move data. Consumption may record use. Neither is treated as the sole authority over the structural admission decision.

---

## 1. Reference Files

The reference implementation consists of:

`reference/stile_delivery_admission_v2_1.py`

`reference/STILE_Delivery_Admission_Browser_Demo_v2_1.html`

Reference identity:

`Profile: STILE-DELIVERY-ADMISSION-1-D01`

`Schema: 2.1.0`

---

## 2. Run the Python Reference

From the repository root:

```text
python reference/stile_delivery_admission_v2_1.py
```

Expected final result:

```text
Conformance: 25/25 PASS
```

For the conformance report only:

```text
python reference/stile_delivery_admission_v2_1.py --self-test
```

Expected:

`status = PASS`

`passed = 25`

`total = 25`

---

## 3. Open the Browser Reference

### Option A - Local HTTP Server

From the repository root:

```text
python -m http.server 8000
```

Then open:

```text
http://localhost:8000/reference/STILE_Delivery_Admission_Browser_Demo_v2_1.html
```

### Option B - Direct Open

Open this file directly in a modern browser:

```text
reference/STILE_Delivery_Admission_Browser_Demo_v2_1.html
```

The browser application is self-contained and does not require an API, server-side resolver, external JavaScript library, or external stylesheet.

---

## 4. Built-In Browser Conformance

The browser runs its conformance suite automatically.

Expected:

```text
25/25 PASS
```

The built-in checks cover:

- aligned structural resolution;
- structural admission;
- transport-observation separation;
- consumption-observation separation;
- deterministic replay;
- key-order invariance;
- incomplete-state abstention;
- conflict handling;
- structural-change sensitivity;
- explicit invalid-observation handling;
- Unicode canonicalization fixtures.

---

## 5. Expected Demonstration Cases

| Case | Resolution | Delivery Admission | Transport Observation | Consumption Observation | Reason Codes |
|---|---|---|---|---|---|
| Aligned | RESOLVED | ADMITTED | NOT_OBSERVED | UNKNOWN | NONE |
| Transport observed | RESOLVED | ADMITTED | RECEIVED | UNKNOWN | NONE |
| Consumed | RESOLVED | ADMITTED | RECEIVED | CONSUMED | NONE |
| Incomplete | INCOMPLETE | ABSTAIN | NOT_OBSERVED | UNKNOWN | MISSING_RECEIVER_ID |
| Identity conflict | CONFLICT | ABSTAIN | NOT_OBSERVED | UNKNOWN | MESSAGE_ID_MISMATCH |
| Payload conflict | CONFLICT | ABSTAIN | NOT_OBSERVED | UNKNOWN | PAYLOAD_HASH_MISMATCH |
| Intent conflict | CONFLICT | ABSTAIN | NOT_OBSERVED | UNKNOWN | INTENT_EXPECTATION_MISMATCH |
| Explicit conflict | CONFLICT | ABSTAIN | NOT_OBSERVED | UNKNOWN | EXPLICIT_CONFLICT |

---

## 6. Structural Resolution Model

The governing relation is:

`structural_delivery_state = resolve(declared_delivery_structure, versioned_rules)`

The bounded resolution states are:

`complete + consistent -> RESOLVED + ADMITTED`

`incomplete -> INCOMPLETE + ABSTAIN`

`conflicting -> CONFLICT + ABSTAIN`

The model does not equate structural admission with physical transmission or later consumption.

---

## 7. Three Independent Evidence Identities

STILE v2.1 produces three SHA-256 identities.

### Structure Hash

`structure_hash`

Identifies the declared structural core together with the profile and schema.

Transport and consumption observations are not included in this hash.

### Decision Hash

`decision_hash`

Identifies:

- the profile;
- the schema;
- the structure hash;
- the resolution;
- the delivery admission;
- the reason codes.

### Observation Hash

`observation_hash`

Binds transport and consumption observations to the decision hash without rewriting the structural decision.

Therefore:

`same structure + different transport observation -> same structure_hash + same decision_hash + different observation_hash`

and:

`same structure + different consumption observation -> same structure_hash + same decision_hash + different observation_hash`

---

## 8. Baseline Cross-Runtime Hash Parity

For the canonical aligned baseline, Python and the browser must produce exactly:

```text
structure_hash:
bd8b71f05dc106fb7d85e85d5d9f26c80c58800fb64e00b7b05a87eaa0fea943

decision_hash:
6e400f99186b39b1ad97603502ea398276a84e04e56e746b528d2af8a6fb6994

observation_hash:
54faa92e594b183abfb2dd99da1eda0abb20be52fe1650adba3a685a611d8823
```

These hashes are version-bound because the schema version is part of the hashed structure.

---

## 9. Unicode Cross-Runtime Hash Parity

The Unicode fixture must produce exactly:

```text
structure_hash:
7f8373ff19549acdd2d6aabaaca4b586756b1d1ec11291cd350237e45e60fc8d

decision_hash:
8e7108d66e658dfbc65a33e45060e96f2fc1392f085d53f7934ba691b589afce

observation_hash:
c34d6d177369c495eab86c25ce124e4c8f72852289a9175dfbf1d0ce4923cd6f
```

This confirms matching UTF-8 canonical hashing for the declared fixture across the Python and browser implementations.

---

## 10. Full Browser Audit

Open the browser developer console and paste:

```javascript
console.clear();

(() => {
  const base = baseStructure();

  const baseline = resolveDelivery(base);

  const received = resolveDelivery({
    ...base,
    transport_observation: "RECEIVED"
  });

  const consumed = resolveDelivery({
    ...base,
    transport_observation: "RECEIVED",
    consumption_observation: "CONSUMED"
  });

  const invalidTransport = resolveDelivery({
    ...base,
    transport_observation: "BROKEN"
  });

  const invalidConsumption = resolveDelivery({
    ...base,
    consumption_observation: "BROKEN"
  });

  const unicodeResult = resolveDelivery(unicodeStructure());

  const reordered = {
    consumption_observation: base.consumption_observation,
    context_id: base.context_id,
    receiver_expectation: base.receiver_expectation,
    sender_intent: base.sender_intent,
    receiver_expected_payload_hash: base.receiver_expected_payload_hash,
    sender_payload_hash: base.sender_payload_hash,
    receiver_expected_message_id: base.receiver_expected_message_id,
    sender_message_id: base.sender_message_id,
    receiver_id: base.receiver_id,
    sender_id: base.sender_id,
    transport_observation: base.transport_observation,
    conflict: base.conflict
  };

  const tests = [
    ["aligned_structure_resolves",
      baseline.resolution === "RESOLVED"],

    ["aligned_structure_is_admitted",
      baseline.delivery_admission === "ADMITTED"],

    ["transport_does_not_change_structure_hash",
      baseline.structure_hash === received.structure_hash],

    ["transport_does_not_change_decision_hash",
      baseline.decision_hash === received.decision_hash],

    ["transport_changes_observation_hash",
      baseline.observation_hash !== received.observation_hash],

    ["consumption_does_not_change_structure_hash",
      received.structure_hash === consumed.structure_hash],

    ["consumption_does_not_change_decision_hash",
      received.decision_hash === consumed.decision_hash],

    ["consumption_changes_observation_hash",
      received.observation_hash !== consumed.observation_hash],

    ["same_structure_same_decision_hash",
      baseline.decision_hash === resolveDelivery(base).decision_hash],

    ["key_order_invariant",
      baseline.decision_hash === resolveDelivery(reordered).decision_hash],

    ["missing_receiver_is_incomplete",
      resolveDelivery(withoutField(base, "receiver_id")).resolution === "INCOMPLETE"],

    ["missing_receiver_abstains",
      resolveDelivery(withoutField(base, "receiver_id")).delivery_admission === "ABSTAIN"],

    ["empty_message_id_is_incomplete",
      resolveDelivery({...base, sender_message_id: ""}).resolution === "INCOMPLETE"],

    ["null_intent_is_incomplete",
      resolveDelivery({...base, sender_intent: null}).resolution === "INCOMPLETE"],

    ["invalid_conflict_type_is_incomplete",
      resolveDelivery({...base, conflict: "false"}).resolution === "INCOMPLETE"],

    ["message_identity_mismatch_conflicts",
      resolveDelivery({
        ...base,
        receiver_expected_message_id: "MSG-999"
      }).resolution === "CONFLICT"],

    ["payload_mismatch_conflicts",
      resolveDelivery({
        ...base,
        receiver_expected_payload_hash: "PAYLOAD-OTHER"
      }).resolution === "CONFLICT"],

    ["intent_mismatch_conflicts",
      resolveDelivery({
        ...base,
        receiver_expectation: "DECLINE"
      }).resolution === "CONFLICT"],

    ["explicit_conflict_conflicts",
      resolveDelivery({...base, conflict: true}).resolution === "CONFLICT"],

    ["conflict_abstains",
      resolveDelivery({...base, conflict: true}).delivery_admission === "ABSTAIN"],

    ["structural_change_changes_structure_hash",
      baseline.structure_hash !== resolveDelivery({
        ...base,
        context_id: "ORDER-43"
      }).structure_hash],

    ["structural_change_changes_decision_hash",
      baseline.decision_hash !== resolveDelivery({
        ...base,
        context_id: "ORDER-43"
      }).decision_hash],

    ["invalid_transport_observation_is_explicit",
      invalidTransport.transport_observation === "INVALID"],

    ["invalid_consumption_observation_is_explicit",
      invalidConsumption.consumption_observation === "INVALID"],

    ["python_parity_structure_hash",
      baseline.structure_hash ===
      "bd8b71f05dc106fb7d85e85d5d9f26c80c58800fb64e00b7b05a87eaa0fea943"],

    ["python_parity_decision_hash",
      baseline.decision_hash ===
      "6e400f99186b39b1ad97603502ea398276a84e04e56e746b528d2af8a6fb6994"],

    ["python_parity_observation_hash",
      baseline.observation_hash ===
      "54faa92e594b183abfb2dd99da1eda0abb20be52fe1650adba3a685a611d8823"],

    ["unicode_structure_hash_parity",
      unicodeResult.structure_hash ===
      "7f8373ff19549acdd2d6aabaaca4b586756b1d1ec11291cd350237e45e60fc8d"],

    ["unicode_decision_hash_parity",
      unicodeResult.decision_hash ===
      "8e7108d66e658dfbc65a33e45060e96f2fc1392f085d53f7934ba691b589afce"],

    ["unicode_observation_hash_parity",
      unicodeResult.observation_hash ===
      "c34d6d177369c495eab86c25ce124e4c8f72852289a9175dfbf1d0ce4923cd6f"]
  ];

  const rows = tests.map(([test, pass]) => ({
    test,
    result: pass ? "PASS" : "FAIL"
  }));

  console.table(rows);

  const passed = tests.filter(([, pass]) => pass).length;
  const total = tests.length;
  const status = passed === total ? "PASS" : "FAIL";

  console.log(
    `STILE v2.1 BROWSER AUDIT: ${passed}/${total} ${status}`
  );

  return {
    status,
    passed,
    total,
    baseline,
    received,
    consumed,
    invalidTransport,
    invalidConsumption,
    unicodeResult
  };
})();
```

Expected:

```text
STILE v2.1 BROWSER AUDIT: 30/30 PASS
```

---

## 11. Verify the Three-Lane Invariant

In the browser console:

```javascript
console.clear();

const S = baseStructure();

const A = resolveDelivery(S);

const B = resolveDelivery({
  ...S,
  transport_observation: "RECEIVED"
});

const C = resolveDelivery({
  ...S,
  transport_observation: "RECEIVED",
  consumption_observation: "CONSUMED"
});

console.table([
  {
    case: "BASELINE",
    structure_same: true,
    decision_same: true,
    observation_same: true
  },
  {
    case: "TRANSPORT CHANGED",
    structure_same: A.structure_hash === B.structure_hash,
    decision_same: A.decision_hash === B.decision_hash,
    observation_same: A.observation_hash === B.observation_hash
  },
  {
    case: "CONSUMPTION CHANGED",
    structure_same: A.structure_hash === C.structure_hash,
    decision_same: A.decision_hash === C.decision_hash,
    observation_same: A.observation_hash === C.observation_hash
  }
]);
```

Expected for both changed-observation rows:

```text
structure_same   = true
decision_same    = true
observation_same = false
```

---

## 12. Verify All Eight Browser Cases

In the browser console:

```javascript
console.clear();

console.table(
  cases.map((item, index) => {
    const result = resolveDelivery(item.build());

    return {
      case: index + 1,
      name: item.label,
      resolution: result.resolution,
      admission: result.delivery_admission,
      transport: result.transport_observation,
      consumption: result.consumption_observation,
      reasons: result.reason_codes.join(", ") || "NONE"
    };
  })
);
```

Expected:

```text
Aligned            -> RESOLVED   + ADMITTED
Transport observed -> RESOLVED   + ADMITTED
Consumed           -> RESOLVED   + ADMITTED
Incomplete         -> INCOMPLETE + ABSTAIN
Identity conflict  -> CONFLICT   + ABSTAIN
Payload conflict   -> CONFLICT   + ABSTAIN
Intent conflict    -> CONFLICT   + ABSTAIN
Explicit conflict  -> CONFLICT   + ABSTAIN
```

---

## 13. File Identity

From Windows Command Prompt:

```text
certutil -hashfile reference\stile_delivery_admission_v2_1.py SHA256
certutil -hashfile reference\STILE_Delivery_Admission_Browser_Demo_v2_1.html SHA256
```

Expected file hashes for the verified v2.1 artifacts:

```text
stile_delivery_admission_v2_1.py
SHA256: 7535245810f0e7c7819d55c2e272c8a4098e718b03c82c7e19d9488db9b014d4

STILE_Delivery_Admission_Browser_Demo_v2_1.html
SHA256: efe7207c6dd223495e41849a4eb477c63f624fc4c85f1e3b906cc2836bdb1b9e
```

File hashes identify the exact files.

The STILE structural hashes identify declared structure, structural decisions, and observation records within the reference model.

These are different evidence layers.

---

## 14. Claim Boundary

STILE v2.1 demonstrates a bounded deterministic structural admission model.

It does not claim that:

- physical transmission is unnecessary for systems that must physically transmit data;
- a structural admission proves that bytes reached a remote endpoint;
- a structural admission proves that a recipient read, consumed, or acted on content;
- operational messaging, networking, acknowledgements, retries, queues, or delivery protocols are universally unnecessary.

The reference claim is narrower:

`transport observation is not the sole authority over the bounded structural admission decision`

and:

`consumption observation is not the sole authority over the bounded structural admission decision`

Within the declared profile:

`same declared structure + same versioned rules -> same structural decision`

---

## 15. Final Verification Criteria

A verification run passes when all of the following hold:

- Python conformance reports `25/25 PASS`.
- Browser built-in conformance reports `25/25 PASS`.
- Full browser audit reports `30/30 PASS`.
- All eight demonstration cases match the expected states.
- Python and browser baseline hashes match.
- Python and browser Unicode fixture hashes match.
- Unsupported observations resolve explicitly as `INVALID`.
- Incomplete structure does not produce `ADMITTED`.
- Conflicting structure does not produce `ADMITTED`.
- Transport-only changes do not change the structural decision hash.
- Consumption-only changes do not change the structural decision hash.

---

## Result

STILE v2.1 verifies a deterministic separation between:

`structural delivery admission`

`transport observation`

`consumption observation`

The reference implementation demonstrates that a bounded structural admission decision can remain stable while transport and consumption observations change independently.

`transport establishes movement`

`structure establishes admissibility`

`consumption establishes use`
