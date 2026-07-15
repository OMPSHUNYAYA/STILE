#!/usr/bin/env python3

import argparse
import hashlib
import json
import sys
from pathlib import Path

PROFILE_ID = "STILE-DELIVERY-ADMISSION-1-D01"
SCHEMA_VERSION = "2.1.0"

REQUIRED_STRING_FIELDS = (
    "sender_id",
    "receiver_id",
    "sender_message_id",
    "receiver_expected_message_id",
    "sender_payload_hash",
    "receiver_expected_payload_hash",
    "sender_intent",
    "receiver_expectation",
    "context_id",
)

TRANSPORT_STATES = {
    "UNKNOWN",
    "NOT_OBSERVED",
    "SENT",
    "RECEIVED",
    "FAILED",
}

CONSUMPTION_STATES = {
    "UNKNOWN",
    "UNREAD",
    "CONSUMED",
    "REJECTED",
}


def canonical_json(value):
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )


def sha256_hex(value):
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def normalized_observation(value, allowed):
    if value is None:
        return "UNKNOWN"
    if isinstance(value, str) and value in allowed:
        return value
    return "INVALID"


def extract_structural_core(structure):
    core = {field: structure.get(field) for field in REQUIRED_STRING_FIELDS}
    core["conflict"] = structure.get("conflict")
    return core


def validate_completeness(structure):
    reasons = []

    for field in REQUIRED_STRING_FIELDS:
        if field not in structure:
            reasons.append(f"MISSING_{field.upper()}")
            continue

        value = structure[field]

        if value is None:
            reasons.append(f"NULL_{field.upper()}")
        elif not isinstance(value, str):
            reasons.append(f"INVALID_TYPE_{field.upper()}")
        elif value == "":
            reasons.append(f"EMPTY_{field.upper()}")

    if "conflict" not in structure:
        reasons.append("MISSING_CONFLICT")
    elif structure["conflict"] is None:
        reasons.append("NULL_CONFLICT")
    elif not isinstance(structure["conflict"], bool):
        reasons.append("INVALID_TYPE_CONFLICT")

    return sorted(reasons)


def validate_consistency(structure):
    reasons = []

    if structure["sender_message_id"] != structure["receiver_expected_message_id"]:
        reasons.append("MESSAGE_ID_MISMATCH")

    if structure["sender_payload_hash"] != structure["receiver_expected_payload_hash"]:
        reasons.append("PAYLOAD_HASH_MISMATCH")

    if structure["sender_intent"] != structure["receiver_expectation"]:
        reasons.append("INTENT_EXPECTATION_MISMATCH")

    if structure["conflict"] is not False:
        reasons.append("EXPLICIT_CONFLICT")

    return sorted(reasons)


def resolve_delivery(structure):
    if not isinstance(structure, dict):
        raise TypeError("structure must be a JSON object")

    transport_observation = normalized_observation(
        structure.get("transport_observation"),
        TRANSPORT_STATES,
    )
    consumption_observation = normalized_observation(
        structure.get("consumption_observation"),
        CONSUMPTION_STATES,
    )

    completeness_reasons = validate_completeness(structure)
    core = extract_structural_core(structure)
    structure_hash = sha256_hex(
        {
            "profile_id": PROFILE_ID,
            "schema_version": SCHEMA_VERSION,
            "structural_core": core,
        }
    )

    if completeness_reasons:
        resolution = "INCOMPLETE"
        delivery_admission = "ABSTAIN"
        reason_codes = completeness_reasons
    else:
        consistency_reasons = validate_consistency(structure)

        if consistency_reasons:
            resolution = "CONFLICT"
            delivery_admission = "ABSTAIN"
            reason_codes = consistency_reasons
        else:
            resolution = "RESOLVED"
            delivery_admission = "ADMITTED"
            reason_codes = []

    decision_record = {
        "profile_id": PROFILE_ID,
        "schema_version": SCHEMA_VERSION,
        "structure_hash": structure_hash,
        "resolution": resolution,
        "delivery_admission": delivery_admission,
        "reason_codes": reason_codes,
    }

    decision_hash = sha256_hex(decision_record)

    observation_record = {
        "decision_hash": decision_hash,
        "transport_observation": transport_observation,
        "consumption_observation": consumption_observation,
    }

    observation_hash = sha256_hex(observation_record)

    return {
        "profile_id": PROFILE_ID,
        "schema_version": SCHEMA_VERSION,
        "resolution": resolution,
        "delivery_admission": delivery_admission,
        "reason_codes": reason_codes,
        "structure_hash": structure_hash,
        "decision_hash": decision_hash,
        "transport_observation": transport_observation,
        "consumption_observation": consumption_observation,
        "observation_hash": observation_hash,
    }


def base_structure():
    return {
        "sender_id": "A",
        "receiver_id": "B",
        "sender_message_id": "MSG-001",
        "receiver_expected_message_id": "MSG-001",
        "sender_payload_hash": "PAYLOAD-ABC-001",
        "receiver_expected_payload_hash": "PAYLOAD-ABC-001",
        "sender_intent": "CONFIRM",
        "receiver_expectation": "CONFIRM",
        "context_id": "ORDER-42",
        "conflict": False,
        "transport_observation": "NOT_OBSERVED",
        "consumption_observation": "UNKNOWN",
    }


def unicode_structure():
    return {
        "sender_id": "Å",
        "receiver_id": "用户",
        "sender_message_id": "MSG-Ü-001",
        "receiver_expected_message_id": "MSG-Ü-001",
        "sender_payload_hash": "载荷-Δ-001",
        "receiver_expected_payload_hash": "载荷-Δ-001",
        "sender_intent": "CONFIRM-✓",
        "receiver_expectation": "CONFIRM-✓",
        "context_id": "注文-42",
        "conflict": False,
        "transport_observation": "NOT_OBSERVED",
        "consumption_observation": "UNKNOWN",
    }


def with_changes(structure, **changes):
    result = dict(structure)
    result.update(changes)
    return result


def without(structure, *fields):
    result = dict(structure)
    for field in fields:
        result.pop(field, None)
    return result


def run_conformance():
    base = base_structure()

    no_transport = resolve_delivery(base)
    received = resolve_delivery(
        with_changes(base, transport_observation="RECEIVED")
    )
    consumed = resolve_delivery(
        with_changes(
            base,
            transport_observation="RECEIVED",
            consumption_observation="CONSUMED",
        )
    )

    invalid_transport = resolve_delivery(
        with_changes(base, transport_observation="BROKEN")
    )
    invalid_consumption = resolve_delivery(
        with_changes(base, consumption_observation="BROKEN")
    )
    unicode_result = resolve_delivery(unicode_structure())

    reordered = {
        "consumption_observation": base["consumption_observation"],
        "context_id": base["context_id"],
        "receiver_expectation": base["receiver_expectation"],
        "sender_intent": base["sender_intent"],
        "receiver_expected_payload_hash": base["receiver_expected_payload_hash"],
        "sender_payload_hash": base["sender_payload_hash"],
        "receiver_expected_message_id": base["receiver_expected_message_id"],
        "sender_message_id": base["sender_message_id"],
        "receiver_id": base["receiver_id"],
        "sender_id": base["sender_id"],
        "transport_observation": base["transport_observation"],
        "conflict": base["conflict"],
    }

    checks = []

    def check(name, condition):
        checks.append({"name": name, "pass": bool(condition)})

    check(
        "aligned_structure_resolves",
        no_transport["resolution"] == "RESOLVED",
    )
    check(
        "aligned_structure_is_admitted",
        no_transport["delivery_admission"] == "ADMITTED",
    )
    check(
        "transport_observation_does_not_change_structural_decision",
        no_transport["decision_hash"] == received["decision_hash"],
    )
    check(
        "transport_observation_changes_observation_receipt",
        no_transport["observation_hash"] != received["observation_hash"],
    )
    check(
        "consumption_observation_does_not_change_structural_decision",
        received["decision_hash"] == consumed["decision_hash"],
    )
    check(
        "consumption_observation_changes_observation_receipt",
        received["observation_hash"] != consumed["observation_hash"],
    )
    check(
        "same_structure_same_decision_hash",
        no_transport["decision_hash"] == resolve_delivery(base)["decision_hash"],
    )
    check(
        "key_order_invariant",
        no_transport["decision_hash"] == resolve_delivery(reordered)["decision_hash"],
    )
    check(
        "missing_receiver_is_incomplete",
        resolve_delivery(without(base, "receiver_id"))["resolution"] == "INCOMPLETE",
    )
    check(
        "missing_receiver_abstains",
        resolve_delivery(without(base, "receiver_id"))["delivery_admission"] == "ABSTAIN",
    )
    check(
        "empty_message_id_is_incomplete",
        resolve_delivery(with_changes(base, sender_message_id=""))["resolution"] == "INCOMPLETE",
    )
    check(
        "null_intent_is_incomplete",
        resolve_delivery(with_changes(base, sender_intent=None))["resolution"] == "INCOMPLETE",
    )
    check(
        "invalid_conflict_type_is_incomplete",
        resolve_delivery(with_changes(base, conflict="false"))["resolution"] == "INCOMPLETE",
    )
    check(
        "message_identity_mismatch_conflicts",
        resolve_delivery(
            with_changes(base, receiver_expected_message_id="MSG-999")
        )["resolution"] == "CONFLICT",
    )
    check(
        "payload_mismatch_conflicts",
        resolve_delivery(
            with_changes(base, receiver_expected_payload_hash="PAYLOAD-OTHER")
        )["resolution"] == "CONFLICT",
    )
    check(
        "intent_mismatch_conflicts",
        resolve_delivery(
            with_changes(base, receiver_expectation="DECLINE")
        )["resolution"] == "CONFLICT",
    )
    check(
        "explicit_conflict_conflicts",
        resolve_delivery(with_changes(base, conflict=True))["resolution"] == "CONFLICT",
    )
    check(
        "conflict_abstains",
        resolve_delivery(with_changes(base, conflict=True))["delivery_admission"] == "ABSTAIN",
    )
    check(
        "structural_change_changes_structure_hash",
        no_transport["structure_hash"]
        != resolve_delivery(with_changes(base, context_id="ORDER-43"))["structure_hash"],
    )
    check(
        "structural_change_changes_decision_hash",
        no_transport["decision_hash"]
        != resolve_delivery(with_changes(base, context_id="ORDER-43"))["decision_hash"],
    )
    check(
        "invalid_transport_observation_is_explicit",
        invalid_transport["transport_observation"] == "INVALID",
    )
    check(
        "invalid_consumption_observation_is_explicit",
        invalid_consumption["consumption_observation"] == "INVALID",
    )
    check(
        "unicode_structure_hash_fixture",
        unicode_result["structure_hash"] == "7f8373ff19549acdd2d6aabaaca4b586756b1d1ec11291cd350237e45e60fc8d",
    )
    check(
        "unicode_decision_hash_fixture",
        unicode_result["decision_hash"] == "8e7108d66e658dfbc65a33e45060e96f2fc1392f085d53f7934ba691b589afce",
    )
    check(
        "unicode_observation_hash_fixture",
        unicode_result["observation_hash"] == "c34d6d177369c495eab86c25ce124e4c8f72852289a9175dfbf1d0ce4923cd6f",
    )

    passed = sum(1 for item in checks if item["pass"])
    total = len(checks)

    return {
        "profile_id": PROFILE_ID,
        "schema_version": SCHEMA_VERSION,
        "status": "PASS" if passed == total else "FAIL",
        "passed": passed,
        "total": total,
        "checks": checks,
    }


def showcase_cases():
    base = base_structure()

    cases = [
        (
            "Aligned structure, no transport observed",
            base,
        ),
        (
            "Same structure, transport observed as received",
            with_changes(base, transport_observation="RECEIVED"),
        ),
        (
            "Same structure, consumption observed",
            with_changes(
                base,
                transport_observation="RECEIVED",
                consumption_observation="CONSUMED",
            ),
        ),
        (
            "Incomplete structure",
            without(base, "receiver_id"),
        ),
        (
            "Message identity conflict",
            with_changes(base, receiver_expected_message_id="MSG-999"),
        ),
        (
            "Payload conflict",
            with_changes(base, receiver_expected_payload_hash="PAYLOAD-OTHER"),
        ),
        (
            "Intent conflict",
            with_changes(base, receiver_expectation="DECLINE"),
        ),
        (
            "Explicit conflict",
            with_changes(base, conflict=True),
        ),
    ]

    return [
        {
            "label": label,
            "input": structure,
            "result": resolve_delivery(structure),
        }
        for label, structure in cases
    ]


def print_showcase(cases):
    print("STILE")
    print("Structural Integration Leverage")
    print("Version 2.1")
    print("Delivery-State Resolution Without Transport as the Sole Authority")
    print()
    print(f"Profile: {PROFILE_ID}")
    print(f"Schema:  {SCHEMA_VERSION}")
    print()
    print("Core relations")
    print("  structural_delivery_state = resolve(declared_delivery_structure, versioned_rules)")
    print("  transport establishes movement")
    print("  structure establishes admissibility")
    print("  consumption establishes use")
    print()

    for index, case in enumerate(cases, start=1):
        result = case["result"]
        reasons = ",".join(result["reason_codes"]) if result["reason_codes"] else "NONE"

        print(f"Case {index}: {case['label']}")
        print(f"  resolution:              {result['resolution']}")
        print(f"  delivery_admission:      {result['delivery_admission']}")
        print(f"  transport_observation:   {result['transport_observation']}")
        print(f"  consumption_observation: {result['consumption_observation']}")
        print(f"  reason_codes:            {reasons}")
        print(f"  structure_hash:          {result['structure_hash']}")
        print(f"  decision_hash:           {result['decision_hash']}")
        print(f"  observation_hash:        {result['observation_hash']}")
        print()


def load_structure(path):
    with Path(path).open("r", encoding="utf-8") as handle:
        value = json.load(handle)

    if not isinstance(value, dict):
        raise ValueError("input JSON must contain one object")

    return value


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    try:
        if args.input:
            result = resolve_delivery(load_structure(args.input))
            print(json.dumps(result, indent=2, sort_keys=True))
            return 0

        conformance = run_conformance()

        if args.self_test:
            print(json.dumps(conformance, indent=2, sort_keys=True))
            return 0 if conformance["status"] == "PASS" else 1

        cases = showcase_cases()

        if args.json:
            report = {
                "profile_id": PROFILE_ID,
                "schema_version": SCHEMA_VERSION,
                "conformance": conformance,
                "cases": cases,
            }
            print(json.dumps(report, indent=2, sort_keys=True))
        else:
            print_showcase(cases)
            print(
                f"Conformance: {conformance['passed']}/{conformance['total']} "
                f"{conformance['status']}"
            )

        return 0 if conformance["status"] == "PASS" else 1

    except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
