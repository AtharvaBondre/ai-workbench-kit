"""Release tooling must not accidentally package private outputs or drifted docs."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/'scripts/release_check.py'

class ReleaseTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(SCRIPT.exists(),'Missing release checker')
        spec=importlib.util.spec_from_file_location('release_check',SCRIPT)
        self.r=importlib.util.module_from_spec(spec);spec.loader.exec_module(self.r)
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)

    def test_inventory_excludes_private_outputs_and_git(self):
        for name in ['README.md','profiles.json','.env','reports/usage.json','.git/config','tests/__pycache__/x.pyc','skills/example/SKILL.md']:
            p=self.root/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text('example')
        paths={str(p.relative_to(self.root)) for p in self.r.release_files(self.root)}
        self.assertEqual(paths,{'README.md','skills/example/SKILL.md'})

    def test_release_rejects_symlinks(self):
        (self.root/'README.md').symlink_to('/definitely-not-a-source')
        with self.assertRaises(ValueError):self.r.release_files(self.root)

    def test_manifest_detects_modified_and_added_files(self):
        (self.root/'README.md').write_text('first')
        self.r.update_manifest(self.root)
        self.assertEqual(self.r.check_manifest(self.root),[])
        (self.root/'README.md').write_text('modified')
        self.assertTrue(self.r.check_manifest(self.root))

    def test_privacy_scan_detects_credential_pattern_without_echoing_it(self):
        fake='sk-'+'ant-'+'x'*40
        (self.root/'README.md').write_text(fake)
        findings=self.r.privacy_findings(self.root)
        self.assertEqual(len(findings),1);self.assertNotIn(fake,json.dumps(findings))

    def test_internal_links_are_checked(self):
        (self.root/'README.md').write_text('[Good](https://example.com) [Missing](absent.md)')
        self.assertEqual(len(self.r.link_findings(self.root)),1)

if __name__=='__main__':unittest.main()
