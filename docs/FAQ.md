# ⭐ FAQ — STILE

## Structural Integration Leverage

### Delivery-State Resolution Without Transport as the Sole Authority

**Deterministic • Structure-Based • Bounded Structural Admission**

---

## SECTION A — Purpose & Positioning

### A1. What is STILE?

STILE is a bounded deterministic reference model for structural delivery admission.

It separates three questions:

`Did the data move?`

`Is the declared delivery structure admissible?`

`Was the content later used or consumed?`

These are represented as separate lanes:

`transport_state != structural_delivery_state != consumption_state`

The current STILE profile resolves structural admission from declared structure and versioned rules.

---

### A2. What is the core idea?

The governing relation is:

`structural_delivery_state = resolve(declared_delivery_structure, versioned_rules)`

Within the declared profile:

`same declared structure + same versioned rules -> same structural decision`

---

### A3. What does "without transport as the sole authority" mean?

It means that a transport observation such as `SENT`, `RECEIVED`, or `FAILED` does not by itself determine the bounded structural admission decision.

Transport may establish movement.

Structure establishes admissibility under the current profile.

Consumption may establish later use.

The model keeps these roles separate.

---

### A4. Is STILE saying that communication or networking is unnecessary?

No.

Systems that must physically move data still need an appropriate transport mechanism.

STILE does not claim that:

- bytes can reach a remote endpoint without transmission;
- networking is universally unnecessary;
- acknowledgements or retries are never useful;
- a structural admission proves physical receipt.

The narrower claim is:

`transport observation is not the sole authority over the bounded structural admission decision`

---

### A5. Is STILE a messaging protocol?

No.

STILE is not:

- a network protocol;
- a message broker;
- a queue;
- a retry mechanism;
- a transport replacement;
- a proof of physical receipt.

It is a structural admission model.

---

### A6. Is STILE replacing SMS, APIs, or messaging platforms?

No.

STILE can sit alongside existing systems.

Transport systems may move data.

Receiving systems may record consumption.

STILE resolves a separate question:

`is the declared delivery structure admissible under the named profile and versioned rules?`

---

### A7. What is the current reference profile?

The current profile is:

`STILE-DELIVERY-ADMISSION-1-D01`

The current schema is:

`2.1.0`

---

### A8. What does the current profile evaluate?

The current reference profile evaluates declared structural fields for:

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

---

### A9. What class of problems might STILE help explore?

Potential application directions include:

- APIs and service integration;
- offline-first workflows;
- distributed record exchange;
- financial coordination;
- disaster-response information systems;
- healthcare data workflows;
- IoT state exchange;
- multi-party structural admission.

These are exploration directions. The current profile does not claim to solve every domain-specific delivery problem.

---

## SECTION B — Structural Admission Model

### B1. What is "structure" in STILE?

Structure is the declared set of fields that the active profile treats as relevant to a structural admission decision.

In the current profile, this includes identities, expected identities, intent, expectation, context, and conflict state.

---

### B2. What determines the structural decision?

The current model evaluates whether the declared structure is:

`complete`

and:

`consistent`

The resulting states are:

`complete + consistent -> RESOLVED + ADMITTED`

`incomplete -> INCOMPLETE + ABSTAIN`

`conflicting -> CONFLICT + ABSTAIN`

---

### B3. What does RESOLVED mean?

`RESOLVED` means the required declared structure is complete and consistent under the current profile.

The corresponding delivery admission is:

`ADMITTED`

This is a structural admission result.

It is not a claim of physical transmission or later consumption.

---

### B4. What does INCOMPLETE mean?

`INCOMPLETE` means one or more required structural fields are missing, null, empty, or invalid.

The corresponding delivery admission is:

`ABSTAIN`

The model does not force a positive decision from insufficient structure.

---

### B5. What does CONFLICT mean?

`CONFLICT` means the required structure is complete enough to evaluate, but one or more declared structural relationships disagree.

Examples include:

`MESSAGE_ID_MISMATCH`

`PAYLOAD_HASH_MISMATCH`

`INTENT_EXPECTATION_MISMATCH`

`EXPLICIT_CONFLICT`

The corresponding delivery admission is:

`ABSTAIN`

---

### B6. Why is abstention important?

Abstention prevents the model from turning missing or conflicting structure into an unsupported positive admission.

The safety rule is:

`incomplete -> no ADMITTED result`

`conflicting -> no ADMITTED result`

---

### B7. Who defines the structure?

The domain or application profile defines the relevant fields and rules.

STILE evaluates the declared structure under those rules.

It does not invent domain truth.

---

## SECTION C — Three Independent Lanes

### C1. What is the structural admission lane?

The structural admission lane resolves the declared structure under the active profile and schema.

It produces:

- `resolution`;
- `delivery_admission`;
- `reason_codes`;
- `structure_hash`;
- `decision_hash`.

---

### C2. What is the transport observation lane?

The transport observation lane records operational movement separately from the structural decision.

The current reference values are:

`UNKNOWN`

`NOT_OBSERVED`

`SENT`

`RECEIVED`

`FAILED`

Unsupported values are surfaced as:

`INVALID`

---

### C3. What is the consumption observation lane?

The consumption observation lane records later use separately from the structural decision.

The current reference values are:

`UNKNOWN`

`UNREAD`

`CONSUMED`

`REJECTED`

Unsupported values are surfaced as:

`INVALID`

---

### C4. Can transport change without changing the structural decision?

Yes.

The current invariant is:

`transport-only change -> same structure_hash + same decision_hash + different observation_hash`

---

### C5. Can consumption change without changing the structural decision?

Yes.

The current invariant is:

`consumption-only change -> same structure_hash + same decision_hash + different observation_hash`

---

### C6. Why separate these lanes?

Because movement, admissibility, and use answer different questions.

Collapsing them into one state can hide important distinctions.

STILE makes those distinctions explicit.

---

## SECTION D — Evidence Identities

### D1. What is structure_hash?

`structure_hash` identifies the declared structural core together with the profile and schema.

Transport and consumption observations are outside this hash.

---

### D2. What is decision_hash?

`decision_hash` identifies:

- the profile;
- the schema;
- the structure hash;
- the resolution;
- the delivery admission;
- the reason codes.

---

### D3. What is observation_hash?

`observation_hash` binds transport and consumption observations to the structural decision.

This allows observations to change without rewriting the structural decision.

---

### D4. What is the core deterministic guarantee?

Within the declared profile and schema:

`same declared structure + same versioned rules -> same structural decision`

The implementation also verifies deterministic hash reproduction for declared fixtures.

---

### D5. Does changing the schema change the hashes?

Yes.

The evidence model is version-bound.

The structure identity includes:

`profile + schema + declared structure`

A schema change therefore intentionally changes the associated hashes.

---

### D6. Does key order change the result?

No, for equivalent JSON object content under the canonical serialization used by the reference implementation.

The conformance suite verifies key-order invariance.

---

### D7. Does STILE support Unicode consistently?

The v2.1 reference pair uses matching UTF-8 canonical hashing.

The Python and browser implementations verify the same Unicode fixture hashes.

---

## SECTION E — Determinism & Cross-Runtime Parity

### E1. Is STILE deterministic?

Yes, within the declared profile, schema, input structure, and rules.

---

### E2. Will the Python and browser references agree?

The verified v2.1 fixtures do.

The reference pair verifies:

`baseline cross-runtime hash parity -> PASS`

`Unicode cross-runtime hash parity -> PASS`

---

### E3. What conformance results should I expect?

The current reference results are:

`Python conformance -> 25/25 PASS`

`Browser built-in conformance -> 25/25 PASS`

`Full browser audit -> 30/30 PASS`

`Visible demonstration cases -> 8/8 expected`

---

### E4. Why does the browser show 25/25 while the full audit shows 30/30?

The browser application contains a built-in 25-check conformance suite.

The broader console audit additionally checks explicit `structure_hash` stability across transport-only and consumption-only changes, together with exact Python/browser parity for the three canonical baseline hashes.

This brings the total to 30 checks.

Both are intentional.

---

## SECTION F — Practical Meaning

### F1. What changes conceptually?

Instead of treating one operational signal as the whole truth, STILE separates:

`movement`

`structural admissibility`

`use`

This makes the authority boundary explicit.

---

### F2. What are the practical benefits of this separation?

Potential benefits include:

- deterministic structural admission;
- explicit abstention on incomplete input;
- explicit conflict handling;
- clearer state boundaries;
- independent observation tracking;
- reproducible evidence identities;
- easier cross-runtime verification.

Actual production benefits depend on the surrounding domain and implementation.

---

### F3. What is the role of transport?

Transport establishes movement.

It may be essential for systems that need to move data.

STILE simply does not make transport observation the sole authority over structural admission.

---

### F4. What is the role of consumption?

Consumption establishes later use or handling.

A message may be structurally admitted before, after, or independently of a later consumption observation, depending on the surrounding application.

---

## SECTION G — Boundaries

### G1. Does ADMITTED mean that bytes reached another machine?

No.

`ADMITTED` is a structural result under the current profile.

It does not prove remote receipt.

---

### G2. Does ADMITTED mean that a person read the content?

No.

Reading or use belongs to the consumption lane.

---

### G3. Does RECEIVED automatically mean ADMITTED?

No.

Transport observation and structural admission are separate.

---

### G4. Does CONSUMED automatically mean ADMITTED?

Not by definition.

Consumption observation and structural admission are separate lanes.

---

### G5. Is STILE a universal delivery oracle?

No.

The current profile is explicitly bounded.

Other domains may require different fields, rules, authorities, and evidence models.

---

### G6. Is STILE a consensus protocol?

No.

It does not implement distributed consensus, finality, quorum agreement, or network coordination.

---

### G7. Is STILE a proof of legal or contractual delivery?

No.

Legal meaning depends on applicable law, policy, evidence requirements, and domain-specific rules.

The reference implementation does not establish legal delivery.

---

## SECTION H — Skeptic Questions

### H1. Isn't this just a rules engine?

The implementation does evaluate explicit rules.

The research contribution being demonstrated is the state separation and deterministic evidence model:

`transport_state != structural_delivery_state != consumption_state`

together with:

`same declared structure + same versioned rules -> same structural decision`

Whether a production deployment uses a rules engine, dedicated service, embedded library, or another implementation mechanism is a separate engineering choice.

---

### H2. Is the result still produced by computation?

Yes.

The reference implementation computes the result.

The claim is not that computation disappears.

The claim is about which declared information is authoritative for the bounded structural admission decision.

---

### H3. Can STILE fail?

Yes.

A deployment can be wrong if:

- the profile is poorly designed;
- required fields are omitted;
- domain rules are incorrect;
- inputs are false or untrusted;
- implementation behavior diverges from the declared profile;
- the model is applied outside its intended scope.

Determinism does not guarantee that a badly specified model is correct for a domain.

---

### H4. Does same structure always mean same real-world truth?

Not necessarily.

The deterministic guarantee applies to the resolver's bounded decision under the declared profile and rules.

Real-world truth may depend on facts or authorities that are not represented in the declared structure.

---

### H5. Why are unsupported observations marked INVALID?

Because an unrecognized observation should not silently become a recognized state.

This makes unsupported values explicit and keeps Python and browser behavior aligned.

---

## SECTION I — Verification

### I1. How is the Python reference verified?

Run:

`python reference/stile_delivery_admission_v2_1.py --self-test`

Expected:

`status = PASS`

`passed = 25`

`total = 25`

---

### I2. How is the browser reference verified?

The browser runs its built-in conformance suite automatically.

Expected:

`25/25 PASS`

The verification guide also provides the full console audit.

Expected:

`30/30 PASS`

---

### I3. What does the full browser audit verify?

It verifies:

- aligned structural resolution;
- structural admission;
- transport separation;
- consumption separation;
- deterministic replay;
- key-order invariance;
- incomplete-state abstention;
- conflict handling;
- structural-change sensitivity;
- invalid observation handling;
- Python/browser baseline hash parity;
- Unicode hash parity.

---

### I4. How can I verify the exact reference files?

Use the SHA-256 identities recorded in the freeze file and compare them against hashes generated locally.

The verification guide contains the exact commands and expected values.

---

## SECTION J — Adoption & Packaging

### J1. Is STILE a production system?

No.

STILE v2.1 is a bounded reference implementation and research model.

A production deployment would require domain-specific requirements, security controls, trust assumptions, operational handling, monitoring, testing, and governance.

---

### J2. Why keep the reference implementation small?

A compact reference makes the governing behavior easier to inspect, reproduce, test, and port.

The current goal is clarity of the structural model, not feature breadth.

---

### J3. Can STILE be extended?

Yes.

Possible directions include:

- additional structural fields;
- domain-specific profiles;
- multi-party admission;
- stronger certificate formats;
- independent language ports;
- profile conformance suites;
- application-specific trust models.

Any extension should preserve clear versioning and claim boundaries.

---

## SECTION K — Shunyaya Framework Context

### K1. How does STILE fit within the Shunyaya Framework?

STILE contributes a specific structural separation:

`transport establishes movement`

`structure establishes admissibility`

`consumption establishes use`

Its focus is not removing operational systems.

Its focus is preventing one operational mechanism from automatically becoming the sole authority over a bounded structural admission decision.

---

### K2. What is the main STILE invariant?

Within the declared profile:

`same declared structure + same versioned rules -> same structural decision`

---

### K3. What is the strongest accurate one-line description?

STILE is a deterministic structural admission model that separates delivery-state resolution from transport and consumption observations, allowing the bounded structural decision to remain stable while those observations change independently.

---

## ⭐ Final One-Line Summary

STILE v2.1 deterministically resolves whether declared delivery structure is admissible under a named profile and schema, while keeping transport movement and later consumption as separate observations rather than treating either as the sole authority over the structural decision.
