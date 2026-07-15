# ⭐ STILE — Architecture Notes

## Structural Integration Leverage

### Delivery-State Resolution Without Transport as the Sole Authority

**Deterministic • Structure-Based • Bounded Structural Admission**

---

## 1. Architectural Purpose

STILE defines a bounded structural admission architecture that separates:

`transport movement`

`structural admissibility`

`consumption`

The core separation is:

`transport_state != structural_delivery_state != consumption_state`

The architecture is designed so that transport and consumption observations can change without automatically rewriting the bounded structural admission decision.

The governing relation is:

`structural_delivery_state = resolve(declared_delivery_structure, versioned_rules)`

Within the declared profile:

`same declared structure + same versioned rules -> same structural decision`

---

## 2. Reference Identity

The current reference architecture is defined by:

`Profile: STILE-DELIVERY-ADMISSION-1-D01`

`Schema: 2.1.0`

The current implementation resolves three structural outcomes:

`complete + consistent -> RESOLVED + ADMITTED`

`incomplete -> INCOMPLETE + ABSTAIN`

`conflicting -> CONFLICT + ABSTAIN`

The model is intentionally bounded to its declared profile and rules.

---

## 3. High-Level Architecture

STILE separates the system into three independent lanes.

### 3.1 Structural Admission Lane

Responsible for:

- evaluating declared structural fields;
- checking completeness;
- checking consistency;
- producing a bounded structural decision;
- producing structural and decision evidence identities.

Outputs include:

`resolution`

`delivery_admission`

`reason_codes`

`structure_hash`

`decision_hash`

The structural admission lane does not use transport or consumption observations as inputs to its decision logic.

---

### 3.2 Transport Observation Lane

Responsible for recording operational movement.

Current reference states are:

`UNKNOWN`

`NOT_OBSERVED`

`SENT`

`RECEIVED`

`FAILED`

Unsupported values are normalized to:

`INVALID`

Transport observations are not included in the structural core.

They do not independently alter:

`resolution`

`delivery_admission`

`reason_codes`

`structure_hash`

`decision_hash`

They are represented only in the observation evidence layer.

---

### 3.3 Consumption Observation Lane

Responsible for recording later use or handling.

Current reference states are:

`UNKNOWN`

`UNREAD`

`CONSUMED`

`REJECTED`

Unsupported values are normalized to:

`INVALID`

Consumption observations do not independently alter:

`resolution`

`delivery_admission`

`reason_codes`

`structure_hash`

`decision_hash`

They are represented only in the observation evidence layer.

---

## 4. Structural Data Model

The current structural core contains:

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

The resolver also accepts:

`transport_observation`

`consumption_observation`

These two observational fields are deliberately outside the structural core.

---

## 5. Completeness Model

The required structural string fields must be:

- present;
- non-null;
- strings;
- non-empty.

The `conflict` field must be:

- present;
- non-null;
- Boolean.

If these requirements are not satisfied:

`resolution = INCOMPLETE`

`delivery_admission = ABSTAIN`

The resolver emits deterministic reason codes such as:

`MISSING_RECEIVER_ID`

`EMPTY_SENDER_MESSAGE_ID`

`NULL_SENDER_INTENT`

`INVALID_TYPE_CONFLICT`

The architecture therefore does not infer missing structural support.

---

## 6. Consistency Model

For complete structure, the current profile requires:

`sender_message_id = receiver_expected_message_id`

`sender_payload_hash = receiver_expected_payload_hash`

`sender_intent = receiver_expectation`

`conflict = false`

If one or more conditions fail:

`resolution = CONFLICT`

`delivery_admission = ABSTAIN`

Possible reason codes include:

`MESSAGE_ID_MISMATCH`

`PAYLOAD_HASH_MISMATCH`

`INTENT_EXPECTATION_MISMATCH`

`EXPLICIT_CONFLICT`

The architecture therefore does not convert contradiction into positive admission.

---

## 7. Structural Admission Rule

The structural decision is defined by three mutually exclusive branches:

`not complete -> INCOMPLETE + ABSTAIN`

`complete AND not consistent -> CONFLICT + ABSTAIN`

`complete AND consistent -> RESOLVED + ADMITTED`

This creates a deterministic bounded admission result for each accepted input structure under the active profile and schema.

---

## 8. Evidence Architecture

STILE v2.1 produces three SHA-256 evidence identities.

### 8.1 Structure Hash

The structure record is:

`StructureRecord = {profile_id, schema_version, structural_core}`

The structure identity is:

`structure_hash = SHA256(canonical_json(StructureRecord))`

This binds the declared structural core to the active profile and schema.

Transport and consumption observations are not included.

---

### 8.2 Decision Hash

The decision record is:

`DecisionRecord = {profile_id, schema_version, structure_hash, resolution, delivery_admission, reason_codes}`

The decision identity is:

`decision_hash = SHA256(canonical_json(DecisionRecord))`

This binds the bounded structural decision to the exact version-bound structure identity.

---

### 8.3 Observation Hash

The observation record is:

`ObservationRecord = {decision_hash, transport_observation, consumption_observation}`

The observation identity is:

`observation_hash = SHA256(canonical_json(ObservationRecord))`

This allows transport and consumption observations to change without rewriting the structural decision identity.

---

## 9. Lane-Separation Invariants

For a transport-only change:

`same structural core`

`different transport observation`

the architecture preserves:

`same structure_hash`

`same decision_hash`

while:

`observation_hash`

may change.

Therefore:

`transport-only change -> same structural decision`

For a consumption-only change:

`same structural core`

`different consumption observation`

the architecture also preserves:

`same structure_hash`

`same decision_hash`

while:

`observation_hash`

may change.

Therefore:

`consumption-only change -> same structural decision`

---

## 10. Deterministic Properties

Within the same profile, schema, canonicalization, rules, and accepted input:

`same declared structure -> same structural decision`

`same canonical structure record -> same structure_hash`

`same canonical decision record -> same decision_hash`

`same canonical observation record -> same observation_hash`

Repeated evaluation is stable:

`same input replay -> same structural decision and same evidence identities`

The current conformance suite also verifies property-order invariance for equivalent reference objects.

---

## 11. Canonicalization and Cross-Runtime Parity

The Python and browser references use matching canonical JSON behavior for the declared object model.

The v2.1 pair verifies:

`baseline cross-runtime hash parity -> PASS`

`Unicode cross-runtime hash parity -> PASS`

The current profile uses fixed ASCII field names and supports Unicode string values.

This parity claim is bounded to the declared canonicalization model and tested fixtures.

It is not a claim that all serialization formats are automatically equivalent.

---

## 12. Version Binding

The profile and schema are part of the hashed structure record.

Therefore:

`profile + schema + structural core -> structure_hash`

A schema change intentionally changes the version-bound evidence identity.

This prevents evidence generated under one schema from silently presenting itself as evidence generated under another schema.

---

## 13. Safety Architecture

### 13.1 Incomplete-State Safety

`incomplete -> INCOMPLETE + ABSTAIN`

Guarantee within the declared profile:

`incomplete structure -> no ADMITTED result`

---

### 13.2 Conflict Safety

`conflicting -> CONFLICT + ABSTAIN`

Guarantee within the declared profile:

`conflicting structure -> no ADMITTED result`

---

### 13.3 Positive Admission

`complete + consistent -> RESOLVED + ADMITTED`

Positive admission is therefore bounded by the profile's declared completeness and consistency rules.

---

## 14. Authority Boundaries

STILE does not collapse all system state into one authority.

### Transport establishes movement

Transport may be operationally necessary when data must physically move.

### Structure establishes admissibility

The structural lane determines whether the declared structure is admissible under the active profile.

### Consumption establishes use

Consumption records later reading, acceptance, rejection, or use.

The architecture therefore avoids treating any one of these as the entire system truth.

---

## 15. Architectural Claim Boundary

STILE v2.1 does not claim that:

- physical transmission is unnecessary where data must move;
- structural admission proves remote receipt;
- structural admission proves human reading or consumption;
- transport systems are universally unnecessary;
- acknowledgements and retries are universally unnecessary;
- the current profile is a universal delivery oracle;
- deterministic resolution guarantees that declared inputs are factually true;
- the model provides distributed consensus, finality, or legal delivery.

The bounded architectural claim is:

`transport observation is not the sole authority over the bounded structural admission decision`

and:

`consumption observation is not the sole authority over the bounded structural admission decision`

---

## 16. Practical Deployment Pattern

A deployment may use STILE alongside existing systems.

Transport systems may:

- move data;
- record network events;
- produce transport observations.

Receiving systems may:

- record unread state;
- record consumption;
- record rejection.

STILE resolves a separate bounded question:

`is the declared delivery structure admissible under the named profile and versioned rules?`

This separation allows existing operational systems to remain in place while structural admission is handled independently.

---

## 17. Reference Verification

The current reference pair has been verified with:

`Python conformance -> 25/25 PASS`

`Browser built-in conformance -> 25/25 PASS`

`Full browser audit -> 30/30 PASS`

`Visible demonstration cases -> 8/8 expected`

`Baseline cross-runtime hash parity -> PASS`

`Unicode cross-runtime hash parity -> PASS`

`Invalid observation handling parity -> PASS`

These results establish conformance of the current reference implementation to the declared v2.1 behavior.

---

## 18. Architectural Extension Points

Possible future extensions include:

- additional structural fields;
- domain-specific profiles;
- multi-party structural admission;
- stronger certificate formats;
- independent language ports;
- richer conformance suites;
- application-specific trust models;
- explicit upstream authority models.

Any extension should preserve:

`clear profile identity`

`clear schema identity`

`deterministic rules`

`explicit claim boundaries`

`separation between structural decisions and observations`

---

## 19. Relationship to the Shunyaya Framework

STILE is developed within the Shunyaya Framework.

Its architectural contribution is the explicit separation:

`transport establishes movement`

`structure establishes admissibility`

`consumption establishes use`

The focus is not the removal of operational systems.

The focus is the prevention of one operational mechanism from automatically becoming the sole authority over a bounded structural admission decision.

---

## 20. Final Architectural Statement

STILE v2.1 defines a deterministic structural admission architecture in which complete and consistent declared structure produces `RESOLVED + ADMITTED`, incomplete structure produces `INCOMPLETE + ABSTAIN`, and conflicting structure produces `CONFLICT + ABSTAIN`.

Transport and consumption remain separate observation lanes.

The architecture preserves the bounded invariant:

`same declared structure + same versioned rules -> same structural decision`

while allowing:

`transport observation`

and:

`consumption observation`

to change independently without rewriting that structural decision.
