#!/usr/bin/env python3
"""Check a clean distribution without reading any live app/account configuration."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile

ROOT=Path(__file__).resolve().parents[1]
MANIFEST='validation/FILES.sha256.json'
ROOT_FILES={'README.md','LICENSE','AGENTS.md','CONTRIBUTING.md','SECURITY.md','SUPPORT.md',
            'CODE_OF_CONDUCT.md','CHANGELOG.md','ROADMAP.md','.gitignore','.nojekyll',
            'index.html','START-HERE.html','workbench.py','build_guide.py'}
DIRECTORIES={'.github','skills','tests','scripts','validation'}
EXCLUDED={'.git','__pycache__','.venv','.pytest_cache','private','reports','dist'}

def release_files(root):
    files=[]
    for path in sorted(root.rglob('*')):
        rel=path.relative_to(root)
        if any(part in EXCLUDED for part in rel.parts):continue
        if path.is_symlink():raise ValueError('Symlink in release source: '+str(rel))
        if not path.is_file():continue
        if path.name in {'profiles.json','.DS_Store'} or path.name.startswith(('.env','credentials')) or path.suffix in {'.pyc','.zip','.log','.pem','.key'}:continue
        if (len(rel.parts)==1 and path.name in ROOT_FILES) or (len(rel.parts)>1 and rel.parts[0] in DIRECTORIES):files.append(path)
    return files

def expected_manifest(root):
    return {'release':'0.2.0','files':{str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in release_files(root) if str(p.relative_to(root))!=MANIFEST}}

def update_manifest(root):
    target=root/MANIFEST;target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(json.dumps(expected_manifest(root),indent=2)+'\n')

def check_manifest(root):
    try:actual=json.loads((root/MANIFEST).read_text())
    except (OSError,ValueError):return ['Missing or invalid release manifest.']
    expected=expected_manifest(root)
    if actual==expected:return []
    a=actual.get('files',{});e=expected['files']
    return ['Manifest differs: '+name for name in sorted(set(a)|set(e)) if a.get(name)!=e.get(name)] or ['Manifest release metadata differs.']

def privacy_findings(root):
    patterns={
      'provider credential':r'\b(?:AKIA|ASIA)[A-Z0-9]{16}\b|sk-ant-[A-Za-z0-9_-]{20,}|gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}',
      'private key':r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',
      'personal home path':r'/(?:Users|home)/(?!example(?:/|[\s\x27\x22])|runner(?:/|[\s\x27\x22]))[A-Za-z0-9._-]+/',
    }
    findings=[]
    for path in release_files(root):
        if str(path.relative_to(root))==MANIFEST:continue
        text=path.read_text(encoding='utf-8')
        for name,regex in patterns.items():
            if re.search(regex,text):findings.append({'file':str(path.relative_to(root)),'check':name})
    return findings

def link_findings(root):
    findings=[]
    for path in release_files(root):
        if path.suffix!='.md':continue
        for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',path.read_text()):
            if target.startswith(('https:','http:','mailto:','#')):continue
            target=target.split('#')[0]
            if target and not (path.parent/target).exists():findings.append({'file':str(path.relative_to(root)),'missing_link':target})
    return findings

def guide_current(root):
    with tempfile.TemporaryDirectory() as temp:
        destination=Path(temp)
        shutil.copy2(root/'build_guide.py',destination/'build_guide.py')
        shutil.copytree(root/'skills/ai-workbench/references',destination/'skills/ai-workbench/references')
        proc=subprocess.run([sys.executable,str(destination/'build_guide.py')],capture_output=True,text=True)
        return proc.returncode==0 and (destination/'START-HERE.html').read_bytes()==(root/'START-HERE.html').read_bytes()

def package(root,output):
    output=Path(output).expanduser().absolute()
    if output.exists():raise ValueError('Archive already exists; choose another filename.')
    with zipfile.ZipFile(output,'x',zipfile.ZIP_DEFLATED) as archive:
        for path in release_files(root):archive.write(path,str(Path('ai-workbench-kit')/path.relative_to(root)))
    with zipfile.ZipFile(output) as archive:
        if archive.testzip():raise ValueError('Archive integrity check failed.')
    return {'archive':str(output),'bytes':output.stat().st_size,'sha256':hashlib.sha256(output.read_bytes()).hexdigest()}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--update-manifest',action='store_true')
    parser.add_argument('--package',metavar='NEW_ZIP_PATH')
    args=parser.parse_args()
    try:
        issues=privacy_findings(ROOT)+link_findings(ROOT)
        if not guide_current(ROOT):issues.append('Generated visual guide is stale; run python3 build_guide.py.')
        if issues:print(json.dumps({'issues':issues},indent=2));return 1
        if args.update_manifest:update_manifest(ROOT)
        issues=check_manifest(ROOT)
        if issues:print(json.dumps({'issues':issues},indent=2));return 1
        result={'release_files':len(release_files(ROOT)),'links':'passed','privacy_patterns':'passed','guide':'current','manifest':'matched'}
        if args.package:result['package']=package(ROOT,args.package)
        print(json.dumps(result,indent=2));return 0
    except (OSError,ValueError) as error:
        print('Release check stopped: '+str(error),file=sys.stderr);return 1

if __name__=='__main__':raise SystemExit(main())
