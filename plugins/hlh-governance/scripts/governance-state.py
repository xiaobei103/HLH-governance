"""Validate a minimal governance position and calculate its resume gate."""
import argparse, json

REQUIRED = ["record_type", "task", "risk", "lifecycle_node", "current_gate", "authorization", "permission", "evidence_state", "findings_state", "completion_state", "next_authorized_action"]
INVALIDATE = ("authorization_changed", "scope_changed", "permission_changed", "risk_changed", "evidence_invalidated", "protected_action_added")

def validate(data):
    errors = ["missing:" + k for k in REQUIRED if k not in data]
    if data.get("record_type") != "governance-state": errors.append("record_type must be governance-state")
    if data.get("risk") not in {"LOW", "MEDIUM", "HIGH", "UNKNOWN"}: errors.append("risk must be LOW/MEDIUM/HIGH/UNKNOWN")
    return errors

def resume_gate(data):
    if data.get("risk") == "UNKNOWN" or any(data.get(k) for k in INVALIDATE): return "preflight"
    if data.get("findings_state") not in (None, "none", "closed"): return "finding-closure"
    if data.get("completion_state") == "incomplete": return data["next_authorized_action"]
    return data["current_gate"]

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("file"); args = ap.parse_args()
    try:
        with open(args.file, encoding="utf-8") as stream: data = json.load(stream)
    except Exception:
        print(json.dumps({"status":"FAIL","error":"invalid JSON"})); return 2
    errors = validate(data); result = {"status":"PASS" if not errors else "FAIL", "errors":errors}
    if not errors: result["resume_gate"] = resume_gate(data)
    print(json.dumps(result, ensure_ascii=False)); return 0 if not errors else 2
if __name__ == "__main__": raise SystemExit(main())
