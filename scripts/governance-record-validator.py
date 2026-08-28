"""Validate bounded HLH governance records without side effects."""
import argparse, json
def missing(d, keys): return [k for k in keys if k not in d]
def validate(d):
    e=[]; kind=d.get("record_type")
    if kind=="role-transition":
        e += ["missing:"+x for x in missing(d,["role","scope","permission","authorization","single_write_authority"])]
        if d.get("role")=="Builder" and d.get("permission")!="Write Authority": e.append("Builder requires Write Authority")
        if d.get("single_write_authority") is not True: e.append("single_write_authority must be true")
    elif kind=="handoff":
        e += ["missing:"+x for x in missing(d,["handoff_type","head","branch","status","staged","untracked","work_package","owner","scope","completed","incomplete","risks","evidence","next_action","incoming_role","incoming_permission","incoming_authorization"])]
        if d.get("handoff_type")=="controlled-dirty":
            e += ["missing:"+x for x in missing(d,["dirty_changes"])]
            if d.get("dirty_changes") and any(missing(x,["file","status","owner","work_package","reason","action"]) for x in d["dirty_changes"]): e.append("dirty_changes require six fields")
    elif kind=="completion":
        e += ["missing:"+x for x in missing(d,["main_agent","scope","self_verify","findings_closed","completion_decision","production_readiness_decision"])]
        if d.get("independent_audit_required") and not d.get("independent_audit_evidence"): e.append("independent audit evidence required")
        if d.get("findings_closed") is not True: e.append("findings must be closed")
        if d.get("production_readiness_decision")=="implied": e.append("production readiness cannot be implied")
    elif kind=="runtime":
        e += ["missing:"+x for x in missing(d,["requested_model","actual_model","requested_capability","actual_capability","evidence_state"])]
        if d.get("actual_model") in (None,"UNKNOWN") or d.get("actual_capability") in (None,"UNKNOWN"): e.append("actual runtime must be known")
    elif kind=="finding-closure":
        e += ["missing:"+x for x in missing(d,["finding_id","original_condition","remediation","verification_evidence","residual_risk","closure_decision"])]
    elif kind=="delegation":
        e += ["missing:"+x for x in missing(d,["task","scope","lifecycle_role","specialty_role","permission","owner","expected_output","stop_conditions"])]
        if d.get("lifecycle_role")=="Auditor" and d.get("permission")!="Read-only": e.append("Auditor must be read-only")
        if d.get("lifecycle_role")!="Builder" and d.get("permission")=="Write Authority": e.append("non-Builder cannot have Write Authority")
    elif kind=="execution-review":
        e += ["missing:"+x for x in missing(d,["declared_scope","role","permission","result","evidence","findings","runtime_record"])]
    else: e.append("unsupported record_type")
    return e
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("file"); a=ap.parse_args()
    try:
        with open(a.file,encoding="utf-8") as f: d=json.load(f)
    except Exception: print(json.dumps({"status":"FAIL","error":"invalid JSON"})); return 2
    e=validate(d); print(json.dumps({"status":"PASS" if not e else "FAIL","errors":e},ensure_ascii=False)); return 0 if not e else 2
if __name__=="__main__": raise SystemExit(main())
