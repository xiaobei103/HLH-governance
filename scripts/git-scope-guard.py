"""Report whether a declared path scope matches the Git working tree."""
import argparse, json, subprocess
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--scope', nargs='+', required=True); ap.add_argument('--repo', default='.')
    a=ap.parse_args(); r=subprocess.run(['git','-C',a.repo,'status','--short'],text=True,capture_output=True,check=False)
    paths=[line[3:] for line in r.stdout.splitlines() if len(line)>=4]
    allow_all='.' in a.scope or './' in a.scope
    outside=[] if allow_all else [x for x in paths if not any(x==s or x.startswith(s.rstrip('/')+'/' ) for s in a.scope)]
    print(json.dumps({'status':'PASS' if not outside else 'FAIL','changed_paths':paths,'outside_scope':outside},ensure_ascii=False))
    return 0 if not outside else 2
if __name__=='__main__': raise SystemExit(main())
