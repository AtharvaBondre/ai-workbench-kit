"""Synthetic fixtures only: no account calls or access to live app configuration."""
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / 'skills/ai-workbench/scripts/workbench.py'

class WorkbenchTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(TOOL.exists(), 'Missing toolkit implementation')
        spec = importlib.util.spec_from_file_location('wb', TOOL)
        self.w = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.w)
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def test_child_environment_isolated_without_changing_parent(self):
        source = {'PATH': '/bin', 'HOME': '/home/example', 'ANTHROPIC_API_KEY': 'secret',
                  'AWS_PROFILE': 'customer', 'AWS_ACCESS_KEY_ID': 'secret',
                  'AZURE_CLIENT_SECRET': 'secret', 'ANTHROPIC_MODEL': 'wrong',
                  'CLAUDE_CODE_USE_BEDROCK': '1', 'CLAUDE_CODE_OAUTH_TOKEN': 'secret',
                  'CLAUDE_CONFIG_DIR': '/old/store', 'EDITOR': 'vi'}
        result = self.w.child_environment(source, {'kind':'subscription'})
        self.assertEqual(source['AWS_PROFILE'], 'customer')
        self.assertEqual(result, {'PATH':'/bin','HOME':'/home/example','CLAUDE_CONFIG_DIR':'/old/store','EDITOR':'vi'})

    def test_bedrock_sets_only_explicit_profile_and_region(self):
        result = self.w.child_environment({'AWS_PROFILE':'wrong'}, {'kind':'bedrock','aws_profile':'coding','region':'us-west-2'})
        self.assertEqual(result, {'CLAUDE_CODE_USE_BEDROCK':'1','AWS_PROFILE':'coding','AWS_REGION':'us-west-2','AWS_DEFAULT_REGION':'us-west-2'})

    def test_api_profile_never_accepts_literal_keys(self):
        with self.assertRaises(self.w.SafeError):
            self.w.validate_profile({'kind':'api','api_key':'sk-private'})

    def test_profile_rejects_missing_identity_and_unknown_fields(self):
        for p in [{'kind':'subscription'}, {'kind':'bedrock'}, {'kind':'foundry'},
                  {'kind':'subscription','email':'x@example.com','organization_id':'org1','env':{}}]:
            with self.subTest(p=p), self.assertRaises(self.w.SafeError):
                self.w.validate_profile(p)

    def test_private_write_is_exclusive_and_rejects_symlink(self):
        p = self.root/'private.json'
        self.w.private_json(p, {'ok':True})
        self.assertEqual(p.stat().st_mode & 0o777, 0o600)
        with self.assertRaises(self.w.SafeError): self.w.private_json(p, {'ok':False})
        link = self.root/'link'; link.symlink_to(p)
        with self.assertRaises(self.w.SafeError): self.w.private_json(link, {})
        self.assertEqual(json.loads(p.read_text()), {'ok':True})

    def test_manifest_detects_append_edit_missing_and_new_without_copying(self):
        folder = self.root/'sessions'; folder.mkdir()
        for name in ['append','edit','missing','unchanged']: (folder/name).write_text('original\n')
        baseline = self.w.snapshot([folder])
        (folder/'append').write_text('original\nnext\n')
        (folder/'edit').write_text('modified\n')
        (folder/'missing').unlink(); (folder/'new').write_text('new')
        result = self.w.compare_snapshot(baseline)
        self.assertEqual(result['counts'], {'unchanged':1,'appended':1,'changed':1,'missing':1,'new':1})
        self.assertNotIn('original\n', json.dumps(baseline))

    def test_manifest_refuses_links_and_missing_paths(self):
        f = self.root/'f'; f.write_text('x'); link = self.root/'link'; link.symlink_to(f)
        for p in [link, self.root/'absent']:
            with self.assertRaises(self.w.SafeError): self.w.snapshot([p])

    def test_api_environment_key_never_appears_in_plan(self):
        profile={'kind':'api','key_env':'WORKBENCH_TEST_KEY'}
        self.w.validate_profile(profile)
        env=self.w.child_environment({'WORKBENCH_TEST_KEY':'private'},profile)
        self.assertNotIn('ANTHROPIC_API_KEY', env)

    def test_settings_conflict_is_reported_without_values(self):
        cfg = self.root/'settings.json'
        cfg.write_text(json.dumps({'env':{'ANTHROPIC_BASE_URL':'https://private.example','CLAUDE_CODE_USE_BEDROCK':'1'},'apiKeyHelper':'secret-command'}))
        found = self.w.settings_conflicts([cfg])
        self.assertEqual(len(found),3)
        self.assertNotIn('secret-command',json.dumps(found))
        self.assertNotIn('private.example',json.dumps(found))

    def test_subscription_schema_fails_closed(self):
        profile={'kind':'subscription','email':'person@example.com','organization_id':'org-a'}
        self.w.check_subscription({'loggedIn':True,'authMethod':'claude.ai','email':'person@example.com','orgId':'org-a'}, profile)
        for result in [{}, {'loggedIn':True,'authMethod':'api_key','email':'person@example.com','orgId':'org-a'},
                       {'loggedIn':True,'authMethod':'claude.ai','email':'other@example.com','orgId':'org-a'}]:
            with self.assertRaises(self.w.SafeError): self.w.check_subscription(result,profile)

    def test_aws_mismatch_stops_and_never_falls_back(self):
        p={'kind':'bedrock','aws_profile':'coding','region':'us-west-2','account_id':'123456789012','principal_arn':'arn:aws:iam::123456789012:user/coding'}
        with patch.object(self.w,'run_json',return_value={'Account':'wrong','Arn':'wrong'}) as run:
            with self.assertRaises(self.w.SafeError): self.w.verify_identity(p,{},self.root)
        self.assertEqual(run.call_count,1)
        self.assertIn('--profile',run.call_args.args[0]); self.assertIn('--region',run.call_args.args[0])

    def test_claude_usage_deduplicates_streamed_messages_and_counts_cache(self):
        f=self.root/'claude.jsonl'
        rows=[{'timestamp':'2026-01-02T00:00:00Z','sessionId':'s','type':'assistant','message':{'id':'m','model':'sonnet-example','usage':{'input_tokens':10,'cache_read_input_tokens':90,'cache_creation_input_tokens':0,'output_tokens':2}}}]
        rows.append(json.loads(json.dumps(rows[0]))); rows[1]['message']['usage']['output_tokens']=5
        f.write_text('\n'.join(json.dumps(r) for r in rows))
        result=self.w.usage_report([f],'claude',self.w.parse_time('2026-01-01T00:00:00Z'))
        self.assertEqual(result['input_tokens'],100); self.assertEqual(result['output_tokens'],5)
        self.assertEqual(result['cache_hit_percent'],90.0); self.assertEqual(result['requests'],1)
        self.assertNotIn('message',result)

    def test_codex_usage_uses_delta_not_sum_of_cumulative_snapshots(self):
        f=self.root/'codex.jsonl'
        def row(t,n,c,o):return {'timestamp':t,'type':'event_msg','payload':{'type':'token_count','info':{'total_token_usage':{'input_tokens':n,'cached_input_tokens':c,'output_tokens':o}}}}
        f.write_text('\n'.join(json.dumps(r) for r in [row('2026-01-01T00:00:00Z',100,50,10),row('2026-01-02T00:00:00Z',120,65,14),row('2026-01-02T00:00:00Z',120,65,14),row('2026-01-03T00:00:00Z',150,90,20)]))
        result=self.w.usage_report([f],'codex',self.w.parse_time('2026-01-02T00:00:00Z'))
        self.assertEqual(result['input_tokens'],50); self.assertEqual(result['cached_input_tokens'],40); self.assertEqual(result['output_tokens'],10)

    def test_usage_bad_schema_does_not_claim_zero_healthy(self):
        f=self.root/'unknown.jsonl'; f.write_text('{"newSchema":1}\nnot-json')
        report=self.w.usage_report([f],'claude',self.w.parse_time('2026-01-01T00:00:00Z'))
        self.assertEqual(report['status'],'insufficient-data'); self.assertIsNone(report['cache_hit_percent'])
        self.assertGreater(report['malformed_lines'],0)

    def test_skill_install_never_overwrites_and_is_preview_by_default(self):
        target=self.root/'skills'
        result=self.w.install_skill(target,False)
        self.assertFalse(target.exists()); self.assertEqual(result['action'],'preview')
        result=self.w.install_skill(target,True)
        self.assertTrue((target/'ai-workbench/SKILL.md').is_file())
        with self.assertRaises(self.w.SafeError): self.w.install_skill(target,True)

    def test_invalid_codex_record_does_not_replace_valid_baseline(self):
        f=self.root/'codex.jsonl'
        values=[{'input_tokens':100,'cached_input_tokens':50,'output_tokens':10},
                {'cached_input_tokens':60,'output_tokens':20},
                {'input_tokens':200,'cached_input_tokens':70,'output_tokens':30}]
        f.write_text('\n'.join(json.dumps({'timestamp':'2026-01-02T00:00:00Z','payload':{'type':'token_count','info':{'total_token_usage':v}}}) for v in values))
        r=self.w.usage_report([f],'codex',self.w.parse_time('2026-01-01T00:00:00Z'))
        self.assertEqual((r['input_tokens'],r['cached_input_tokens'],r['output_tokens']),(100,20,20))
        self.assertEqual(r['skipped_usage_records'],1); self.assertEqual(r['status'],'partial-data')

    def test_claude_empty_usage_is_insufficient_not_observed_zero(self):
        f=self.root/'claude.jsonl'
        f.write_text(json.dumps({'timestamp':'2026-01-02T00:00:00Z','type':'assistant','message':{'id':'m','usage':{}}}))
        r=self.w.usage_report([f],'claude',self.w.parse_time('2026-01-01T00:00:00Z'))
        self.assertEqual(r['status'],'insufficient-data'); self.assertEqual(r['skipped_usage_records'],1)

    def test_relative_config_dir_is_rejected(self):
        with self.assertRaises(self.w.SafeError): self.w.settings_paths(self.root,{'CLAUDE_CONFIG_DIR':'relative-store'})

    def test_null_subscription_identity_is_safe_error(self):
        with self.assertRaises(self.w.SafeError):
            self.w.check_subscription({'loggedIn':True,'authMethod':'claude.ai','email':None,'orgId':'org-a'},{'email':'x@example.com','organization_id':'org-a'})

    def test_null_azure_identity_is_safe_error(self):
        p={'kind':'foundry','subscription_id':'a','tenant_id':'b','azure_account':'x@example.com'}
        with patch.object(self.w,'run_json',return_value={'id':'a','tenantId':'b','user':None}):
            with self.assertRaises(self.w.SafeError): self.w.verify_identity(p,{},self.root)

    def test_installed_skill_has_same_command_entrypoint(self):
        self.w.install_skill(self.root/'skills',True)
        import subprocess
        r=subprocess.run([os.sys.executable,str(self.root/'skills/ai-workbench/workbench.py'),'--version'],capture_output=True,text=True)
        self.assertEqual(r.returncode,0); self.assertIn('0.1.0',r.stdout)

    def test_model_cannot_be_a_cli_flag(self):
        with self.assertRaises(self.w.SafeError): self.w.validate_profile({'kind':'api','key_env':'EXAMPLE_KEY','model':'--dangerously-skip-permissions'})

if __name__=='__main__': unittest.main()
