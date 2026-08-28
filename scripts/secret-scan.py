"""Safe synthetic secret scan; never prints matching values."""
import argparse, json, re, pathlib
PATTERNS=[r'AKIA[0-9A-Z]{16}',r'(?i)api[_-]?key\s*[:=]\s*[^\s]+',r'(?i)token\s*[:=]\s*[^\s]+',r'(?i)password\s*[:=]\s*[^\s]+',r'(?i)DATABASE_URL\s*[:=]\s*[^\s]+']
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('paths',nargs='+'); a=ap.parse_args(); hits=[]
    for raw in a.paths:
        p=pathlib.Path(raw)
        if p.is_file() and any(re.search(x,p.read_text(errors='ignore')) for x in PATTERNS): hits.append(str(p))
    print(json.dumps({'status':'PASS' if not hits else 'FAIL','matching_files':hits,'values_exposed':False},ensure_ascii=False))
    return 0 if not hits else 2
if __name__=='__main__': raise SystemExit(main())
