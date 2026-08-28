"""Capture and validate persistent runtime evidence for triggered scenarios."""
import argparse, datetime, json, subprocess

REQUIRED = ['evidence_state', 'timestamp_utc', 'command', 'exit_code', 'persistent']

def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest='action', required=True)
    capture = sub.add_parser('capture')
    capture.add_argument('--output', required=True)
    capture.add_argument('command', nargs='+')
    validate = sub.add_parser('validate')
    validate.add_argument('file')
    args = ap.parse_args()
    if args.action == 'capture':
        result = subprocess.run(args.command, text=True, capture_output=True, check=False)
        record = {'evidence_state': 'ACTUAL_RUNTIME_EVIDENCE',
                  'timestamp_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  'command': args.command, 'exit_code': result.returncode,
                  'stdout': result.stdout, 'stderr': result.stderr, 'persistent': True}
        with open(args.output, 'w', encoding='utf-8') as stream:
            json.dump(record, stream, ensure_ascii=False, indent=2)
        print(json.dumps({'status': 'PASS', 'output': args.output, 'exit_code': result.returncode}))
        return result.returncode
    with open(args.file, encoding='utf-8') as stream:
        data = json.load(stream)
    missing = [key for key in REQUIRED if key not in data]
    print(json.dumps({'status': 'PASS' if not missing else 'FAIL', 'missing': missing}))
    return 0 if not missing else 2

if __name__ == '__main__':
    raise SystemExit(main())
