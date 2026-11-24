"""Guided setup uses synthetic answers, never live credentials or applications."""
import argparse
import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]

class OnboardingTests(unittest.TestCase):
    def setUp(self):
        spec=importlib.util.spec_from_file_location('wb',ROOT/'skills/ai-workbench/scripts/workbench.py')
        self.w=importlib.util.module_from_spec(spec);spec.loader.exec_module(self.w)
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)

    def configure(self,answers,output=None):
        self.assertTrue(hasattr(self.w,'configure'),'Missing guided configuration workflow')
        output=output or self.root/'private'/'profiles.json'; stream=io.StringIO()
        with patch('builtins.input',side_effect=answers),contextlib.redirect_stdout(stream):
            self.w.configure(argparse.Namespace(output=str(output)))
        return output,stream.getvalue()

    def test_api_wizard_writes_only_after_explicit_save(self):
        output,display=self.configure(['2','','1','EXAMPLE_API_KEY','','save'])
        self.assertEqual(json.loads(output.read_text()),{'version':1,'profiles':{'api':{'kind':'api','key_env':'EXAMPLE_API_KEY'}}})
        self.assertEqual(output.stat().st_mode & 0o777,0o600)
        self.assertEqual(output.parent.stat().st_mode & 0o777,0o700)
        self.assertIn('check-config',display);self.assertIn('Desktop',display)

    def test_cancel_wizard_creates_nothing(self):
        output,display=self.configure(['1','personal','person@example.com','org-example','','cancel'])
        self.assertFalse(output.parent.exists());self.assertIn('Nothing saved',display)

    def test_existing_profile_is_not_overwritten(self):
        output=self.root/'profiles.json';output.write_text('preserve')
        self.assertTrue(hasattr(self.w,'configure'))
        with self.assertRaises(self.w.SafeError):self.configure([],output)
        self.assertEqual(output.read_text(),'preserve')

    def test_bedrock_guided_fields(self):
        output,_=self.configure(['3','','coding','us-west-2','123456789012','arn:aws:iam::123456789012:user/coding','example-model','save'])
        p=json.loads(output.read_text())['profiles']['bedrock']
        self.assertEqual(p['aws_profile'],'coding');self.assertEqual(p['model'],'example-model')

    def test_foundry_guided_fields(self):
        output,_=self.configure(['4','','example-resource','sub-example','tenant-example','person@example.com','1','EXAMPLE_FOUNDRY_KEY','example-deployment','save'])
        p=json.loads(output.read_text())['profiles']['foundry']
        self.assertEqual(p['resource'],'example-resource');self.assertEqual(p['key_env'],'EXAMPLE_FOUNDRY_KEY')

    def test_keychain_guided_fields_on_macos(self):
        with patch.object(self.w.sys,'platform','darwin'):
            output,_=self.configure(['2','','2','example-service','example-account','','save'])
        p=json.loads(output.read_text())['profiles']['api']
        self.assertNotIn('key_env',p);self.assertEqual(p['keychain_service'],'example-service')

    def test_malformed_profiles_are_reported_without_echoing_values(self):
        self.assertTrue(hasattr(self.w,'check_config'),'Missing offline config validation')
        p=self.root/'profiles.json';p.write_text(json.dumps({'version':1,'profiles':{'api':{'kind':'api','api_key':'secret-fixture'}}}))
        result=self.w.check_config(p)
        self.assertFalse(result['valid']);self.assertNotIn('secret-fixture',json.dumps(result))

    def test_config_validation_does_not_read_secret_or_call_provider(self):
        self.assertTrue(hasattr(self.w,'check_config'))
        p=self.root/'profiles.json';p.write_text(json.dumps({'version':1,'profiles':{'api':{'kind':'api','key_env':'NOT_SET'}}}))
        with patch.object(self.w,'load_key') as key,patch.object(self.w,'verify_identity') as identity:
            result=self.w.check_config(p)
        self.assertTrue(result['valid']);key.assert_not_called();identity.assert_not_called()
        self.assertEqual(result['authentication'],'not checked')

    def test_profile_missing_fields_are_named(self):
        with self.assertRaises(self.w.SafeError) as error:self.w.validate_profile({'kind':'bedrock'})
        self.assertIn('aws_profile',str(error.exception));self.assertIn('account_id',str(error.exception))

    def test_profile_rejects_secret_looking_values_before_display(self):
        fake='sk-'+'ant-'+'x'*40
        with self.assertRaises(self.w.SafeError):self.w.validate_profile({'kind':'subscription','email':fake,'organization_id':'org-example'})

    def test_config_rejects_empty_or_unknown_top_level(self):
        self.assertTrue(hasattr(self.w,'check_config'))
        for content in [[],{'version':1,'profiles':{}},{'version':1,'profiles':{'api':{'kind':'api','key_env':'TEST_KEY'}},'env':{}}]:
            p=self.root/'profiles.json';p.write_text(json.dumps(content))
            self.assertFalse(self.w.check_config(p)['valid'])

    def test_placeholder_error_names_field(self):
        with self.assertRaises(self.w.SafeError) as error:
            self.w.validate_profile({'kind':'subscription','email':'person@example.com','organization_id':'REPLACE_ORG'})
        self.assertIn('organization_id',str(error.exception))

    def test_malformed_kind_is_safe_error(self):
        with self.assertRaises(self.w.SafeError):self.w.validate_profile({'kind':[]})

    def test_secret_prompt_refuses_noninteractive_input(self):
        self.assertTrue(hasattr(self.w,'prompt_key'))
        with patch.object(self.w.sys.stdin,'isatty',return_value=False):
            with self.assertRaises(self.w.SafeError):self.w.prompt_key()

    def test_secret_prompt_returns_without_printing(self):
        self.assertTrue(hasattr(self.w,'prompt_key'))
        stream=io.StringIO()
        with patch.object(self.w.sys.stdin,'isatty',return_value=True),patch.object(self.w.sys.stderr,'isatty',return_value=True),patch.object(self.w.getpass,'getpass',return_value='synthetic-secret'),contextlib.redirect_stdout(stream):
            self.assertEqual(self.w.prompt_key(),'synthetic-secret')
        self.assertNotIn('synthetic-secret',stream.getvalue())

    def test_empty_keychain_reference_is_invalid(self):
        with self.assertRaises(self.w.SafeError):
            self.w.validate_profile({'kind':'api','keychain_service':'','keychain_account':'account'})

if __name__=='__main__':unittest.main()
