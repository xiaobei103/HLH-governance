import json, shutil, subprocess, sys, tempfile, unittest
from pathlib import Path
ROOT=Path(__file__).parents[1]; PY=sys.executable
def run(script,*args, input=None):
    path=ROOT/script if (ROOT/script).exists() else ROOT/'scripts'/script
    return subprocess.run([PY,str(path),*args],input=input,text=True,capture_output=True)

def run_plugin_preflight_fixture(manifest, hook_file=None):
    with tempfile.TemporaryDirectory() as directory:
        root=Path(directory); (root/'.codex-plugin').mkdir(); (root/'scripts').mkdir()
        (root/'.codex-plugin'/'plugin.json').write_text(json.dumps(manifest),encoding='utf-8')
        if hook_file is not None:
            (root/'hooks.json').write_text(json.dumps(hook_file),encoding='utf-8')
        shutil.copy(ROOT/'scripts'/'plugin-preflight.py',root/'scripts'/'plugin-preflight.py')
        return subprocess.run([PY,str(root/'scripts'/'plugin-preflight.py')],text=True,capture_output=True)

class GovernanceScriptTests(unittest.TestCase):
    def test_hook_manifest_is_valid_and_declares_only_sync_pre_tool_use(self):
        manifest=json.loads((ROOT/'.codex-plugin'/'plugin.json').read_text(encoding='utf-8'))
        self.assertEqual(manifest['hooks'],'./hooks.json')
        hooks=json.loads((ROOT/'hooks.json').read_text(encoding='utf-8'))
        self.assertIn('PreToolUse', hooks['hooks'])
        self.assertNotIn('PostToolUse', hooks['hooks'])
        for group in hooks['hooks']['PreToolUse']:
            for handler in group['hooks']:
                self.assertFalse(handler.get('async',False))

    def test_protected_action_hook_allows_safe_command(self):
        payload={'tool_name':'Bash','tool_input':{'command':'git status --short'}}
        r=run('hooks/protected-action-guard.py', input=json.dumps(payload))
        self.assertEqual(r.returncode,0)
        self.assertEqual(json.loads(r.stdout),{})

    def test_protected_action_hook_denies_commit_without_authorization(self):
        payload={'tool_name':'Bash','tool_input':{'command':'git commit -am "synthetic"'}}
        r=run('hooks/protected-action-guard.py', input=json.dumps(payload))
        self.assertEqual(r.returncode,0)
        result=json.loads(r.stdout)
        self.assertEqual(result['hookSpecificOutput']['permissionDecision'],'deny')
        self.assertNotIn('synthetic', result['hookSpecificOutput']['permissionDecisionReason'])

    def test_protected_action_hook_does_not_false_positive_commit_ish(self):
        payload={'tool_name':'Bash','tool_input':{'command':'git commit-ish'}}
        r=run('hooks/protected-action-guard.py', input=json.dumps(payload))
        self.assertEqual(json.loads(r.stdout),{})

    def test_protected_action_hook_covers_git_protected_forms(self):
        for command in ('git push','git tag','git reset --hard','git -C repo commit -m "x"'):
            with self.subTest(command=command):
                r=run('hooks/protected-action-guard.py', input=json.dumps({'tool_name':'Bash','tool_input':{'command':command}}))
                self.assertEqual(json.loads(r.stdout)['hookSpecificOutput']['permissionDecision'],'deny')

    def test_protected_action_hook_covers_destructive_forms(self):
        for command in ('rm -rf tmp','rm -r -f tmp','Remove-Item -Recurse -Force tmp','Remove-Item -Force -Recurse tmp'):
            with self.subTest(command=command):
                r=run('hooks/protected-action-guard.py', input=json.dumps({'tool_name':'PowerShell','tool_input':{'command':command}}))
                self.assertEqual(json.loads(r.stdout)['hookSpecificOutput']['permissionDecision'],'deny')

    def test_protected_action_hook_handles_case_shell_variants_and_boundaries(self):
        protected={'tool_name':'powershell','tool_input':{'command':'GIT PUSH'}}
        self.assertEqual(json.loads(run('hooks/protected-action-guard.py', input=json.dumps(protected)).stdout)['hookSpecificOutput']['permissionDecision'],'deny')
        for payload in ({'tool_name':'Read','tool_input':{'command':'git push'}},{'tool_name':'Bash'},{'tool_name':'Bash','tool_input':{}},{'tool_name':'Bash','tool_input':{'command':'git "commit-ish'}}):
            with self.subTest(payload=payload):
                self.assertEqual(json.loads(run('hooks/protected-action-guard.py', input=json.dumps(payload)).stdout),{})

    def test_protected_action_hook_handles_malformed_and_empty_input(self):
        for raw in ('{not-json', ''):
            with self.subTest(raw=raw):
                r=run('hooks/protected-action-guard.py', input=raw)
                self.assertEqual(r.returncode,0)
                self.assertEqual(json.loads(r.stdout),{})

    def test_protected_action_hook_supports_shell_tool_variant(self):
        for command, expected in (('echo safe',{}),('git push',{'hookSpecificOutput':{'permissionDecision':'deny'}})):
            with self.subTest(command=command):
                r=run('hooks/protected-action-guard.py', input=json.dumps({'tool_name':'shell','tool_input':{'command':command}}))
                result=json.loads(r.stdout)
                if expected:
                    self.assertEqual(result['hookSpecificOutput']['permissionDecision'],'deny')
                else:
                    self.assertEqual(result,{})

    def test_plugin_preflight_rejects_hook_path_outside_fixture_root(self):
        manifest={'name':'fixture','version':'1.0.0','description':'fixture','author':{},'interface':{},'hooks':'./../outside.json'}
        r=run_plugin_preflight_fixture(manifest)
        self.assertEqual(r.returncode,2)
        self.assertIn('hooks path escapes plugin root',r.stdout)

    def test_plugin_preflight_rejects_missing_hook_target_in_fixture(self):
        manifest={'name':'fixture','version':'1.0.0','description':'fixture','author':{},'interface':{},'hooks':'./missing-hooks.json'}
        r=run_plugin_preflight_fixture(manifest)
        self.assertEqual(r.returncode,2)
        self.assertIn('hooks target does not exist',r.stdout)

    def test_plugin_preflight_accepts_hooks_and_validates_target(self):
        self.assertEqual(run('plugin-preflight.py').returncode,0)

    def test_runtime_context_contract_defines_minimal_loading_boundaries(self):
        policy=(ROOT/'references'/'policies'/'minimal-governance-context.md').read_text(encoding='utf-8')
        for term in ('Always Load','Conditional Load','Never Default Load','LOW','MEDIUM','HIGH','UNKNOWN','history','migration','Feature Parity'):
            self.assertIn(term,policy)

    def test_low_risk_verification_routes_to_skip(self):
        verification=(ROOT/'skills'/'entries'/'governance-verification'/'SKILL.md').read_text(encoding='utf-8')
        self.assertIn('Low Risk',verification); self.assertIn('SKIP',verification)

    def test_medium_and_high_risk_routes_are_explicit(self):
        matrix=(ROOT/'references'/'policies'/'risk-trigger-matrix.md').read_text(encoding='utf-8')
        self.assertIn('MEDIUM',matrix); self.assertIn('HIGH',matrix); self.assertIn('EXECUTE',matrix)
        self.assertIn('production-readiness-review',matrix); self.assertIn('secret-protection-review',matrix)

    def test_unknown_risk_is_inconclusive_and_stops(self):
        matrix=(ROOT/'references'/'policies'/'risk-trigger-matrix.md').read_text(encoding='utf-8')
        preflight=(ROOT/'skills'/'entries'/'governance-preflight'/'SKILL.md').read_text(encoding='utf-8')
        self.assertIn('UNKNOWN',matrix); self.assertIn('INCONCLUSIVE',matrix); self.assertIn('STOP',preflight)

    def test_delivery_convergence_keeps_completion_separate(self):
        delivery=(ROOT/'skills'/'entries'/'delivery-decision'/'SKILL.md').read_text(encoding='utf-8')
        for term in ('Declared Scope','Authorized Scope','Actual Change','Verified Result','Incomplete Items','Out-of-Scope Observations','Next Authorized Action','INCOMPLETE'):
            self.assertIn(term,delivery)
        self.assertIn('Completion != Commit',delivery); self.assertIn('Commit != Production Readiness',delivery)

    def test_low_risk_role_churn_is_conditional(self):
        preflight=(ROOT/'skills'/'entries'/'governance-preflight'/'SKILL.md').read_text(encoding='utf-8')
        self.assertIn('Model ≠ Role ≠ Permission',preflight); self.assertIn('Low Risk',preflight); self.assertIn('Role change',preflight)

    def test_plugin_exposes_only_five_final_skill_entries(self):
        manifest=json.loads((ROOT/'.codex-plugin'/'plugin.json').read_text(encoding='utf-8'))
        self.assertEqual(manifest['skills'],'./skills/entries/')
        expected={'governance-preflight','governance-verification','delivery-decision','secret-protection-review','production-readiness-review'}
        actual={p.name for p in (ROOT/'skills'/'entries').iterdir() if p.is_dir()}
        self.assertEqual(actual,expected)

    def test_low_risk_route_does_not_require_full_verification_chain(self):
        preflight=(ROOT/'skills'/'entries'/'governance-preflight'/'SKILL.md').read_text(encoding='utf-8')
        verification=(ROOT/'skills'/'entries'/'governance-verification'/'SKILL.md').read_text(encoding='utf-8')
        self.assertIn('Scope → Authorization → Risk → Protected Action',preflight)
        self.assertIn('not a default step',verification)

    def test_unified_evidence_tool_supports_triggered_validation(self):
        with tempfile.NamedTemporaryFile('w',delete=False,encoding='utf8') as f:
            json.dump({'evidence_state':'ACTUAL_RUNTIME_EVIDENCE','timestamp_utc':'now','command':['x'],'exit_code':0,'persistent':True},f); name=f.name
        self.assertEqual(run('evidence-bundle.py','validate',name).returncode,0)

    def test_plugin_preflight(self): self.assertEqual(run('plugin-preflight.py').returncode,0)
    def test_scope_guard_clean_scope(self):
        r=run('git-scope-guard.py','--scope','.', '--repo',str(ROOT)); self.assertEqual(r.returncode,0); self.assertIn('"outside_scope": []',r.stdout)
    def test_secret_scan_synthetic_secret(self):
        with tempfile.NamedTemporaryFile('w',delete=False,encoding='utf8') as f:
            f.write('API_KEY=synthetic-value'); name=f.name
        r=run('secret-scan.py',name); self.assertEqual(r.returncode,2); self.assertIn('values_exposed',r.stdout)
    def test_evidence_bundle_validation(self):
        with tempfile.NamedTemporaryFile('w',delete=False,encoding='utf8') as f:
            json.dump({'evidence_state':'ACTUAL_RUNTIME_EVIDENCE','timestamp_utc':'now','command':['x'],'exit_code':0,'persistent':True},f); name=f.name
        self.assertEqual(run('evidence-bundle-validator.py',name).returncode,0)
    def test_governance_record_valid_role_transition(self):
        payload={'record_type':'role-transition','role':'Builder','scope':['skills/'],'permission':'Write Authority','authorization':'user:WP-1','single_write_authority':True}
        with tempfile.NamedTemporaryFile('w',delete=False,encoding='utf8') as f:
            json.dump(payload,f); name=f.name
        self.assertEqual(run('governance-record-validator.py',name).returncode,0)
    def test_governance_record_rejects_multiple_writers(self):
        payload={'record_type':'role-transition','role':'Builder','scope':['skills/'],'permission':'Write Authority','authorization':'user:WP-1','single_write_authority':False}
        with tempfile.NamedTemporaryFile('w',delete=False,encoding='utf8') as f:
            json.dump(payload,f); name=f.name
        self.assertEqual(run('governance-record-validator.py',name).returncode,2)
    def test_governance_record_requires_dirty_handoff_fields(self):
        payload={'record_type':'handoff','handoff_type':'controlled-dirty','head':'abc','branch':'main'}
        with tempfile.NamedTemporaryFile('w',delete=False,encoding='utf8') as f:
            json.dump(payload,f); name=f.name
        self.assertEqual(run('governance-record-validator.py',name).returncode,2)
    def test_governance_record_requires_independent_audit(self):
        payload={'record_type':'completion','main_agent':'builder','self_verify':True,'independent_audit':False,'findings_closed':True,'production_readiness_decision':'separate'}
        with tempfile.NamedTemporaryFile('w',delete=False,encoding='utf8') as f:
            json.dump(payload,f); name=f.name
        self.assertEqual(run('governance-record-validator.py',name).returncode,2)
    def test_governance_record_valid_runtime_reconciliation(self):
        payload={'record_type':'runtime','requested_model':'gpt','actual_model':'gpt','requested_capability':'authorization-preflight','actual_capability':'authorization-preflight','evidence_state':'ACTUAL_RUNTIME_EVIDENCE'}
        with tempfile.NamedTemporaryFile('w',delete=False,encoding='utf8') as f:
            json.dump(payload,f); name=f.name
        self.assertEqual(run('governance-record-validator.py',name).returncode,0)
    def test_governance_record_rejects_auditor_write_permission(self):
        payload={'record_type':'delegation','task':'audit','scope':['.'],'lifecycle_role':'Auditor','specialty_role':'Security','permission':'Write Authority','owner':'main','expected_output':'report','stop_conditions':['scope drift']}
        with tempfile.NamedTemporaryFile('w',delete=False,encoding='utf8') as f:
            json.dump(payload,f); name=f.name
        self.assertEqual(run('governance-record-validator.py',name).returncode,2)

    def test_context_usage_evidence_accepts_metadata_only_record(self):
        payload={'record_type':'context-usage','skill':'governance-preflight','risk':'LOW','lifecycle_node':'preflight','loaded_context':[{'ref':'references/policies/risk-trigger-matrix.md','category':'policy','reason':'risk routing','loaded':True}], 'skipped_context':[{'ref':'references/history/**','category':'history','reason':'LOW default exclusion','loaded':False}], 'trigger':'validation','run_id':'run-1','timestamp_utc':'now'}
        with tempfile.NamedTemporaryFile('w',delete=False,encoding='utf8') as f:
            json.dump(payload,f); name=f.name
        self.assertEqual(run('context-usage-evidence.py',name).returncode,0)

    def test_context_usage_evidence_rejects_sensitive_body(self):
        payload={'record_type':'context-usage','skill':'x','risk':'LOW','lifecycle_node':'preflight','loaded_context':[{'ref':'x','content':'secret'}], 'skipped_context':[], 'trigger':'validation','timestamp_utc':'now'}
        with tempfile.NamedTemporaryFile('w',delete=False,encoding='utf8') as f:
            json.dump(payload,f); name=f.name
        self.assertEqual(run('context-usage-evidence.py',name).returncode,2)

    def test_governance_state_resumes_from_current_gate(self):
        payload={'record_type':'governance-state','task':'t','risk':'MEDIUM','lifecycle_node':'verification','current_gate':'verification','authorization':'valid','permission':'Read-only','evidence_state':'ACTUAL','findings_state':'none','completion_state':'incomplete','next_authorized_action':'delivery'}
        with tempfile.NamedTemporaryFile('w',delete=False,encoding='utf8') as f:
            json.dump(payload,f); name=f.name
        r=run('governance-state.py',name); self.assertEqual(r.returncode,0); self.assertIn('delivery',r.stdout)

    def test_governance_state_restarts_when_scope_changes(self):
        payload={'record_type':'governance-state','task':'t','risk':'LOW','lifecycle_node':'delivery','current_gate':'delivery','authorization':'valid','permission':'Read-only','evidence_state':'ACTUAL','findings_state':'none','completion_state':'incomplete','next_authorized_action':'complete','scope_changed':True}
        with tempfile.NamedTemporaryFile('w',delete=False,encoding='utf8') as f:
            json.dump(payload,f); name=f.name
        r=run('governance-state.py',name); self.assertEqual(r.returncode,0); self.assertIn('preflight',r.stdout)
if __name__=='__main__': unittest.main()
