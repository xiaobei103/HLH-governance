"""Validate optional, metadata-only runtime context selection records."""
import argparse, json

REQUIRED = ["record_type", "skill", "risk", "lifecycle_node", "loaded_context", "skipped_context", "trigger", "timestamp_utc"]
FORBIDDEN = {"content", "body", "text", "stdout", "stderr", "secret", "token", "credential", "value"}
ALLOWED_ITEM = {"ref", "category", "reason", "loaded"}

def validate(data):
    errors = ["missing:" + k for k in REQUIRED if k not in data]
    if data.get("record_type") != "context-usage": errors.append("record_type must be context-usage")
    if data.get("risk") not in {"LOW", "MEDIUM", "HIGH", "UNKNOWN"}: errors.append("risk must be LOW/MEDIUM/HIGH/UNKNOWN")
    for group in ("loaded_context", "skipped_context"):
        if not isinstance(data.get(group), list): errors.append(group + " must be a list"); continue
        for item in data[group]:
            if not isinstance(item, dict): errors.append(group + " items must be objects"); continue
            errors += ["missing-item:" + k for k in ("ref", "category", "reason", "loaded") if k not in item]
            errors += ["forbidden-field:" + k for k in item if k.lower() in FORBIDDEN]
            errors += ["unknown-item-field:" + k for k in item if k not in ALLOWED_ITEM]
    errors += ["forbidden-field:" + k for k in data if k.lower() in FORBIDDEN]
    return errors

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("file"); args = ap.parse_args()
    try:
        with open(args.file, encoding="utf-8") as stream: data = json.load(stream)
    except Exception:
        print(json.dumps({"status":"FAIL","error":"invalid JSON"})); return 2
    errors = validate(data); print(json.dumps({"status":"PASS" if not errors else "FAIL", "errors":errors}, ensure_ascii=False)); return 0 if not errors else 2
if __name__ == "__main__": raise SystemExit(main())
