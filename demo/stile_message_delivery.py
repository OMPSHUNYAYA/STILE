import hashlib

def cert(s):
    raw = "|".join([
        str(s.get("sender")),
        str(s.get("receiver")),
        str(s.get("message_id")),
        str(s.get("intent")),
        str(s.get("expectation"))
    ])
    return hashlib.sha256(raw.encode()).hexdigest()[:16]

rules = [
    ("identity_valid", True,
     lambda s: s.get("message_id") is not None),

    ("intent_match", True,
     lambda s: s.get("intent") == s.get("expectation")),

    ("no_conflict", True,
     lambda s: s.get("conflict") is False),

    ("structure_aligned", True, lambda s:
        s.get("identity_valid") and
        s.get("intent_match") and
        s.get("no_conflict")
    ),

    ("message_delivered",
     lambda s: {
         "message_id": s.get("message_id"),
         "status": "STRUCTURALLY_DELIVERED",
         "sigma": cert(s)
     },
     lambda s: s.get("structure_aligned") is True),
]

state = {
    "sender": "A",
    "receiver": "B",
    "message_id": "MSG-001",
    "intent": "CONFIRM",
    "expectation": "CONFIRM",
    "conflict": False
}

changed = True

while changed:
    changed = False
    for key, value, cond in rules:
        if cond(state):
            new_value = value(state) if callable(value) else value
            if state.get(key) != new_value:
                state[key] = new_value
                changed = True

print(state)