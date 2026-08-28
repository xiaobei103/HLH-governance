"""Capture safe command metadata and output into a JSON evidence record."""
import argparse,datetime,json,subprocess
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--output',required=True); ap.add_argument('command',nargs='+'); a=ap.parse_args()
    r=subprocess.run(a.command,text=True,capture_output=True,check=False)
    record={'evidence_state':'ACTUAL_RUNTIME_EVIDENCE','timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'command':a.command,'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr,'persistent':True}
    with open(a.output,'w',encoding='utf-8') as f: json.dump(record,f,ensure_ascii=False,indent=2)
    print(json.dumps({'status':'PASS','output':a.output,'exit_code':r.returncode},ensure_ascii=False)); return r.returncode
if __name__=='__main__': raise SystemExit(main())
