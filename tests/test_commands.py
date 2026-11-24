"""Exercise command entrypoints and launch orchestration using synthetic state."""
import argparse
import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/'skills/ai-workbench/scripts/workbench.py'

class CommandTests(unittest.TestCase):
    def setUp(self):
        spec=importlib.util.spec_from_file_location('wb',SCRIPT)
        self.w=importlib.util.module_from_spec(spec); spec.loader.exec_module(self.w)
        self.tmp=tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name); self.project=self.root/'original'; self.project.mkdir()

    def call(self,*args):
        return subprocess.run([sys.executable,str(ROOT/'workbench.py'),*map(str,args)],capture_output=True,text=True,env={'HOME':str(self.root),'PATH':os.environ['PATH']})

    def test_non_ai_commands_preserve_originals(self):
        source=self.project/'history.jsonl'; source.write_text('{"type":"user","private_text":"DO_NOT_EXPORT"}\n')
        original=source.read_bytes()
        before=self.root/'before.json'; after=self.root/'after.json'; handoff=self.root/'handoff.json'
        self.assertEqual(self.call('init','--output',self.root/'profiles.json').returncode,0)
        self.assertEqual(self.call('snapshot',source,'--output',before).returncode,0)
        self.assertEqual(self.call('compare',before,'--output',after).returncode,0)
        self.assertEqual(self.call('handoff','--project',self.project,'--sources',source,'--title','Example','--output',handoff).returncode,0)
        self.assertEqual(source.read_bytes(),original)
        self.assertNotIn('DO_NOT_EXPORT',before.read_text()+after.read_text()+handoff.read_text())
        source.write_text('changed')
        self.assertEqual(self.call('compare',before).returncode,3)

    def test_all_five_launch_profiles_use_expected_child_route(self):
        profiles={
            'api':{'kind':'api','key_env':'FIXTURE_KEY','model':'example-model'},
            'foundry':{'kind':'foundry','key_env':'FIXTURE_KEY','resource':'example-resource','subscription_id':'sub','tenant_id':'tenant','azure_account':'person@example.com','model':'example-deployment'},
            'bedrock':{'kind':'bedrock','aws_profile':'coding','region':'us-west-2','account_id':'123456789012','principal_arn':'arn:aws:iam::123456789012:user/coding','model':'example-model'},
            'cloud-pro':{'kind':'subscription','email':'person@example.com','organization_id':'org-a'},
            'cloud-ultra':{'kind':'subscription','email':'other@example.com','organization_id':'org-b'},
        }
        config=self.root/'profiles.json'; config.write_text(json.dumps({'version':1,'profiles':profiles}))
        source={'HOME':str(self.root),'PATH':'/bin','ANTHROPIC_API_KEY':'inherited-not-real','AWS_PROFILE':'wrong-customer','FIXTURE_KEY':'fixture-not-a-real-key'}
        for name,p in profiles.items():
            with self.subTest(profile=name):
                args=argparse.Namespace(config=str(config),profile=name,project=str(self.project),resume='existing-session',execute=True,confirm_idle=True,reviewed_provider_policy=True)
                def fake_identity(command,env,cwd):
                    if command[0]=='aws': return {'Account':p['account_id'],'Arn':p['principal_arn']}
                    if command[0]=='az': return {'id':'sub','tenantId':'tenant','user':{'name':'person@example.com'}}
                    return {'loggedIn':True,'authMethod':'claude.ai','email':p['email'],'orgId':p['organization_id']}
                output=io.StringIO()
                with patch.dict(os.environ,source,clear=True), patch.object(self.w,'settings_paths',return_value=[]), patch.object(self.w.shutil,'which',return_value='/fake/claude'), patch.object(self.w,'run_json',side_effect=fake_identity), patch.object(self.w.subprocess,'call',return_value=0) as child, contextlib.redirect_stdout(output):
                    with self.assertRaises(SystemExit) as ended: self.w.launch(args)
                self.assertEqual(ended.exception.code,0); child.assert_called_once()
                env=child.call_args.kwargs['env']; self.assertEqual(child.call_args.kwargs['cwd'],self.project.resolve())
                self.assertIn('--resume',child.call_args.args[0]); self.assertNotIn('--desktop',child.call_args.args[0])
                if p['kind']=='api': self.assertEqual(env['ANTHROPIC_API_KEY'],'fixture-not-a-real-key'); self.assertNotIn('AWS_PROFILE',env)
                elif p['kind']=='foundry': self.assertEqual(env['ANTHROPIC_FOUNDRY_API_KEY'],'fixture-not-a-real-key'); self.assertNotIn('ANTHROPIC_API_KEY',env)
                elif p['kind']=='bedrock': self.assertEqual(env['AWS_PROFILE'],'coding'); self.assertNotIn('ANTHROPIC_API_KEY',env)
                else: self.assertFalse(any(k.startswith('ANTHROPIC_') or k=='AWS_PROFILE' for k in env))
                self.assertNotIn('fixture-not-a-real-key',output.getvalue())

    def test_preview_never_looks_up_credentials_or_runs_identity(self):
        config=self.root/'profiles.json'; config.write_text(json.dumps({'version':1,'profiles':{'api':{'kind':'api','key_env':'MISSING'}}}))
        args=argparse.Namespace(config=str(config),profile='api',project=str(self.project),resume=None,execute=False)
        with patch.dict(os.environ,{'HOME':str(self.root)},clear=True), patch.object(self.w,'settings_paths',return_value=[]), patch.object(self.w,'verify_identity') as identity, patch.object(self.w,'load_key') as key, contextlib.redirect_stdout(io.StringIO()): self.w.launch(args)
        identity.assert_not_called(); key.assert_not_called()

    def test_settings_conflict_blocks_child_even_with_execute(self):
        config=self.root/'profiles.json'; config.write_text(json.dumps({'version':1,'profiles':{'api':{'kind':'api','key_env':'MISSING'}}}))
        settings=self.project/'settings.json'; settings.write_text('{"env":{"ANTHROPIC_BASE_URL":"https://example.invalid"}}')
        args=argparse.Namespace(config=str(config),profile='api',project=str(self.project),resume=None,execute=True,confirm_idle=True)
        with patch.dict(os.environ,{'HOME':str(self.root)},clear=True), patch.object(self.w,'settings_paths',return_value=[settings]), patch.object(self.w.subprocess,'call') as child, contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaises(self.w.SafeError): self.w.launch(args)
        child.assert_not_called()

if __name__=='__main__': unittest.main()
