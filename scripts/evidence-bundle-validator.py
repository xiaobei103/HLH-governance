import argparse,json
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('file'); a=ap.parse_args(); d=json.load(open(a.file,encoding='utf-8'))
    required=['evidence_state','timestamp_utc','command','exit_code','persistent']; missing=[x for x in required if x not in d]
    print(json.dumps({'status':'PASS' if not missing else 'FAIL','missing':missing},ensure_ascii=False)); return 0 if not missing else 2
if __name__=='__main__': raise SystemExit(main())
