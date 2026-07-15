# 🧩 STILE v2.1 Proof Sketch

## Deterministic Structural Delivery Admission

This document provides a bounded proof sketch for the deterministic properties implemented by STILE v2.1.

STILE separates:

`transport_state != structural_delivery_state != consumption_state`

The structural resolver evaluates declared delivery structure under a named profile and schema.

The governing relation is:

`structural_delivery_state = resolve(declared_delivery_structure, versioned_rules)`

The central guarantee is:

`same declared structure + same versioned rules -> same structural decision`

This proof sketch concerns the bounded structural admission model implemented by:

`Profile: STILE-DELIVERY-ADMISSION-1-D01`

`Schema: 2.1.0`

It does not treat structural admission as proof of physical transmission, remote receipt, later consumption, legal delivery, or distributed consensus.

---

## 1. Model Definition

Let `S` be a declared delivery structure accepted by the reference resolver.

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

The resolver also accepts two observational fields:

`transport_observation`

`consumption_observation`

These observations are intentionally outside the structural core.

The resolver computes:

`R(S) = (resolution, delivery_admission, reason_codes)`

with the bounded state relation:

`complete + consistent -> RESOLVED + ADMITTED`

`incomplete -> INCOMPLETE + ABSTAIN`

`conflicting -> CONFLICT + ABSTAIN`

---

## 2. Completeness Predicate

Let:

`Complete(S)`

mean that every required structural string field is present, non-null, of string type, and non-empty, and that:

`conflict`

is present, non-null, and Boolean.

If `Complete(S)` is false, the resolver returns:

`resolution = INCOMPLETE`

`delivery_admission = ABSTAIN`

with deterministic completeness reason codes.

Therefore:

`not Complete(S) -> not ADMITTED`

This establishes incomplete-state safety within the declared profile.

---

## 3. Consistency Predicate

For complete structure, define:

`Consistent(S)`

to require all of the following:

`sender_message_id = receiver_expected_message_id`

`sender_payload_hash = receiver_expected_payload_hash`

`sender_intent = receiver_expectation`

`conflict = false`

If one or more of these conditions fail, the resolver returns:

`resolution = CONFLICT`

`delivery_admission = ABSTAIN`

with deterministic conflict reason codes.

Therefore:

`Complete(S) AND not Consistent(S) -> not ADMITTED`

This establishes conflict safety within the declared profile.

---

## 4. Structural Admission Rule

For complete and consistent structure:

`Complete(S) AND Consistent(S) -> RESOLVED + ADMITTED`

Combining the three branches:

`not Complete(S) -> INCOMPLETE + ABSTAIN`

`Complete(S) AND not Consistent(S) -> CONFLICT + ABSTAIN`

`Complete(S) AND Consistent(S) -> RESOLVED + ADMITTED`

The branches are mutually exclusive for a given accepted input structure.

Therefore the bounded structural decision is uniquely determined by the declared structure and the active rules.

---

## 5. Deterministic Resolution

For a fixed profile, schema, resolver implementation, and declared structure `S`, every decision branch depends only on deterministic predicates and deterministic reason-code construction.

Therefore:

`S1 = S2 -> R(S1) = R(S2)`

under the same versioned rules.

Equivalently:

`same declared structure + same versioned rules -> same structural decision`

Repeated evaluation does not introduce a new decision source.

Therefore:

`resolve(S) = resolve(S)`

for repeated evaluations of the same accepted input under the same implementation and versioned rules.

---

## 6. Structural and Observational Separation

Let:

`T`

be the normalized transport observation.

Let:

`C`

be the normalized consumption observation.

Neither `T` nor `C` is included in the structural core used to compute:

`structure_hash`

Neither is included in the decision record used to compute:

`decision_hash`

Both are included only in the observation record used to compute:

`observation_hash`

Therefore, for two inputs that differ only in transport observation:

`S_structural_A = S_structural_B`

and:

`T_A != T_B`

the resolver preserves:

`structure_hash_A = structure_hash_B`

`decision_hash_A = decision_hash_B`

while the observation identity may change:

`observation_hash_A != observation_hash_B`

The same relation holds for a consumption-only change.

This proves the implemented authority separation:

`transport-only change -> same structural decision`

`consumption-only change -> same structural decision`

---

## 7. Transport Non-Authority

The structural decision function does not inspect transport observation when evaluating completeness or consistency.

Therefore:

`transport_observation`

cannot independently change:

`resolution`

`delivery_admission`

`reason_codes`

`structure_hash`

`decision_hash`

within the current profile.

Transport may still be operationally important.

The proof is narrower:

`transport observation is not the sole authority over the bounded structural admission decision`

---

## 8. Consumption Non-Authority

The structural decision function does not inspect consumption observation when evaluating completeness or consistency.

Therefore:

`consumption_observation`

cannot independently change:

`resolution`

`delivery_admission`

`reason_codes`

`structure_hash`

`decision_hash`

within the current profile.

Consumption may still be operationally important.

The proof is narrower:

`consumption observation is not the sole authority over the bounded structural admission decision`

---

## 9. Evidence Construction

STILE v2.1 produces three SHA-256 identities.

### 9.1 Structure Identity

The structure record is:

`StructureRecord = {profile_id, schema_version, structural_core}`

Then:

`structure_hash = SHA256(canonical_json(StructureRecord))`

This binds the declared structural core to the named profile and schema.

---

### 9.2 Decision Identity

The decision record is:

`DecisionRecord = {profile_id, schema_version, structure_hash, resolution, delivery_admission, reason_codes}`

Then:

`decision_hash = SHA256(canonical_json(DecisionRecord))`

Therefore the decision identity is bound to:

- the profile;
- the schema;
- the structural core through `structure_hash`;
- the structural resolution;
- the admission state;
- the deterministic reason codes.

---

### 9.3 Observation Identity

The observation record is:

`ObservationRecord = {decision_hash, transport_observation, consumption_observation}`

Then:

`observation_hash = SHA256(canonical_json(ObservationRecord))`

Therefore later observational changes can be represented without rewriting the structural decision identity.

---

## 10. Deterministic Evidence Identity

For the same canonical structure record:

`same StructureRecord -> same structure_hash`

For the same canonical decision record:

`same DecisionRecord -> same decision_hash`

For the same canonical observation record:

`same ObservationRecord -> same observation_hash`

Therefore:

`same declared structure + same versioned rules -> same structural decision -> same decision_hash`

provided the same canonicalization and SHA-256 procedure are used.

This is a deterministic evidence identity.

It is not a proof that the declared inputs are factually true.

---

## 11. Key-Order Invariance

The reference implementation canonicalizes object keys before hashing.

For the fixed ASCII field names used by the current profile:

`same object content in different property order -> same canonical record`

Therefore:

`same canonical content -> same hash`

The conformance suite verifies key-order invariance for the reference fixtures.

This is property-order invariance.

It should not be generalized into a claim that every possible representation in every serialization format is automatically equivalent.

---

## 12. Unicode Cross-Runtime Parity

The Python reference serializes canonical JSON with UTF-8 content preserved.

The browser reference hashes the corresponding canonical UTF-8 representation.

The current profile uses fixed ASCII structural field names and permits Unicode string values.

The declared Unicode fixture produces identical:

`structure_hash`

`decision_hash`

`observation_hash`

in both reference implementations.

Therefore the verified fixture establishes:

`same declared Unicode fixture -> same Python and browser evidence identities`

This is a tested cross-runtime parity claim for the reference implementation.

---

## 13. Invalid Observation Handling

Unsupported transport or consumption observation values are normalized to:

`INVALID`

rather than silently becoming a recognized operational state.

Because these observations remain outside structural admission:

`invalid observation -> structural decision unchanged`

while:

`observation_hash`

records the normalized observation state.

This preserves both explicitness and structural-decision separation.

---

## 14. Version Binding

The profile and schema are included in the structure record.

Therefore:

`same structural values + different schema -> different version-bound structure identity`

in general.

This is intentional.

It prevents evidence generated under one schema from silently presenting itself as evidence generated under another schema.

The governing identity relation is therefore:

`profile + schema + declared structural core -> structure_hash`

---

## 15. Incomplete-State Safety

Suppose a required structural field is absent, null, empty, or invalid.

Then:

`Complete(S) = false`

Therefore:

`resolve(S) -> INCOMPLETE + ABSTAIN`

Hence:

`incomplete structure -> no ADMITTED result`

The resolver does not infer missing structural support.

---

## 16. Conflict Safety

Suppose the structure is complete but one or more consistency conditions fail.

Then:

`Complete(S) = true`

and:

`Consistent(S) = false`

Therefore:

`resolve(S) -> CONFLICT + ABSTAIN`

Hence:

`conflicting structure -> no ADMITTED result`

The resolver does not convert contradiction into a positive admission.

---

## 17. Repetition Stability

Let `S` remain unchanged.

Because the resolver has no random decision source and the structural decision does not depend on mutable transport or consumption history:

`resolve(S)_1 = resolve(S)_2`

for repeated evaluations under the same versioned rules.

The corresponding deterministic records also remain equal.

Therefore:

`same input replay -> same structural decision and same evidence identities`

---

## 18. Independent Resolution

Suppose two independent implementations apply the same profile, schema, canonicalization, hashing procedure, and resolver rules to the same declared structure.

Then the specification requires:

`R_A(S) = R_B(S)`

and matching evidence identities.

The STILE v2.1 Python and browser fixtures verify this requirement for the declared baseline and Unicode cases.

No interaction between the two resolvers is required during the act of resolution once they already possess equivalent declared input.

This does not claim that obtaining equivalent input never requires communication, synchronization, or another upstream mechanism.

---

## 19. What the Hashes Establish

The three hashes provide reproducible identities for:

`declared structural core`

`bounded structural decision`

`bound observation record`

They can be used to compare independently produced reference results.

They do not, by themselves, establish:

- the factual truth of an input declaration;
- physical message transmission;
- remote endpoint receipt;
- human reading or consumption;
- legal delivery;
- distributed consensus;
- finality.

The evidence is only as meaningful as the declared profile, rules, inputs, and trust assumptions surrounding it.

---

## 20. What Is Not Claimed

STILE v2.1 does not prove:

`communication is universally unnecessary`

`networks are unnecessary`

`acknowledgements are unnecessary`

`retries are unnecessary`

`transport can be removed from systems that need physical movement`

`structural admission equals physical receipt`

`structural admission equals consumption`

`structural admission equals legal delivery`

`determinism guarantees factual truth`

The bounded claim is:

`transport observation is not the sole authority over the structural admission decision`

and:

`consumption observation is not the sole authority over the structural admission decision`

---

## 21. Summary of Established Properties

Within `STILE-DELIVERY-ADMISSION-1-D01` under schema `2.1.0`, the reference model establishes:

- deterministic structural resolution;
- explicit `RESOLVED`, `INCOMPLETE`, and `CONFLICT` classification;
- positive admission only for complete and consistent structure;
- abstention for incomplete structure;
- abstention for conflicting structure;
- separation of structural admission from transport observation;
- separation of structural admission from consumption observation;
- deterministic `structure_hash`;
- deterministic `decision_hash`;
- deterministic `observation_hash`;
- key-order invariance for the declared canonical object model;
- explicit invalid-observation handling;
- version-bound evidence identity;
- verified Python/browser parity for the declared baseline and Unicode fixtures;
- stable replay for identical accepted input under identical versioned rules.

The core relation remains:

`same declared structure + same versioned rules -> same structural decision`

---

## Scope Note

This proof sketch applies only to the bounded STILE v2.1 reference model and its declared profile.

It does not replace transport protocols, messaging systems, networking infrastructure, domain-specific trust models, or legal evidence requirements.

Its contribution is the explicit separation of:

`transport movement`

`structural admissibility`

`consumption`

with deterministic structural resolution under declared rules.

---

## 🏁 Final Line

Transport may establish movement.

Structure establishes admissibility under the declared profile.

Consumption may establish use.

STILE keeps these states separate so that none is silently treated as the whole truth.
