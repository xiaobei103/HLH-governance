import json,pathlib,sys
root=pathlib.Path(__file__).parent.parent; manifest=root/'.codex-plugin/plugin.json'; d=json.load(open(manifest,encoding='utf-8'))
required=['name','version','description','author','interface']; missing=[x for x in required if x not in d]
hook_errors=[]
if 'hooks' in d:
    hook_path=d['hooks']
    if not isinstance(hook_path,str) or not hook_path.startswith('./') or pathlib.PurePosixPath(hook_path).is_absolute():
        hook_errors.append('hooks must be a relative ./ path')
    else:
        target=(root/hook_path[2:]).resolve()
        plugin_root=root.resolve()
        if plugin_root not in target.parents:
            hook_errors.append('hooks path escapes plugin root')
        elif not target.is_file():
            hook_errors.append('hooks target does not exist')
        else:
            try:
                data=json.loads(target.read_text(encoding='utf-8'))
                if not isinstance(data.get('hooks'),dict): hook_errors.append('hooks manifest requires an object')
            except (OSError,json.JSONDecodeError) as exc:
                hook_errors.append(f'invalid hooks manifest: {exc}')
print(json.dumps({'status':'PASS' if not missing and not hook_errors else 'FAIL','missing':missing,'hook_errors':hook_errors,'runtime_validation':'NOT_PERFORMED'},ensure_ascii=False)); sys.exit(0 if not missing and not hook_errors else 2)
