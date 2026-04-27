#!/usr/bin/env python3

import hashlib
import json


def normalize(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def cert(value):
    return hashlib.sha256(normalize(value).encode("utf-8")).hexdigest()[:16]


def resolve_otp(structure):
    required = {
        "user_id",
        "expected_hash",
        "provided_hash",
        "window_valid",
        "conflict",
    }

    missing = sorted(k for k in required if k not in structure)
    null_fields = sorted(k for k in required if k in structure and structure[k] is None)

    if missing or null_fields:
        return {
            "resolution": "ABSTAIN",
            "visible_state": "ABSENT",
            "reason_codes": [
                *(f"MISSING_{k.upper()}" for k in missing),
                *(f"NULL_{k.upper()}" for k in null_fields),
            ],
            "sigma": None,
        }

    reason_codes = []

    if structure["expected_hash"] != structure["provided_hash"]:
        reason_codes.append("OTP_HASH_MISMATCH")

    if structure["window_valid"] is not True:
        reason_codes.append("WINDOW_NOT_VALID")

    if structure["conflict"] is not False:
        reason_codes.append("EXPLICIT_CONFLICT_FLAG")

    if reason_codes:
        return {
            "resolution": "CONFLICT",
            "visible_state": "ABSENT",
            "reason_codes": reason_codes,
            "sigma": None,
        }

    visible = {
        "user_id": structure["user_id"],
        "visible_state": "VERIFIED",
        "proof": "OTP_VERIFIED_FROM_STRUCTURE",
    }

    return {
        "resolution": "RESOLVED",
        "visible_state": "VERIFIED",
        "reason_codes": [],
        "sigma": cert(visible),
    }


def show(label, structure):
    result = resolve_otp(structure)
    reason = result["reason_codes"] if result["reason_codes"] else "NONE"
    sigma = result["sigma"] if result["sigma"] else "NONE"

    print(label)
    print(f"  resolution:    {result['resolution']}")
    print(f"  visible_state: {result['visible_state']}")
    print(f"  reason_codes:  {reason}")
    print(f"  sigma:         {sigma}")
    print()


def main():
    print("=== OTP Without Sending — STILE Optional Extension Demo ===\n")

    valid = {
        "user_id": "user-001",
        "expected_hash": "a7f3b9c2d1e8f4a5",
        "provided_hash": "a7f3b9c2d1e8f4a5",
        "window_valid": True,
        "conflict": False,
    }

    show("Valid OTP structure", valid)
    show("Wrong OTP structure", {**valid, "provided_hash": "deadbeef12345678"})
    show("Expired OTP window", {**valid, "window_valid": False})
    show("Explicit conflict", {**valid, "conflict": True})
    show("Missing user_id", {k: v for k, v in valid.items() if k != "user_id"})

    a = resolve_otp(valid)
    b = resolve_otp(valid)

    print("Determinism check")
    print(f"  same structure -> same sigma: {a['sigma'] == b['sigma']}")
    print()
    print("Core insight")
    print("  OTP verification did not come from sending.")
    print("  It emerged from structural alignment.")
    print("  No SMS. No email. No callback. No network dependency.")


if __name__ == "__main__":
    main()