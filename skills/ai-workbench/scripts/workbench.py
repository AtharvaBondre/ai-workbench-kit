#!/usr/bin/env python3
"""AI Workbench Kit: local, dependency-free setup and continuity helpers.

No network calls except identity checks and the interactive Claude child on an
explicit `launch --execute`. No transcript, credential or app-store writes.
"""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

VERSION = '0.1.0'
SKILL = Path(__file__).resolve().parents[1]
class SafeError(Exception): pass

def parse_time(value):
    try:
        d = datetime.fromisoformat(value.replace('Z', '+00:00'))
        return d.replace(tzinfo=timezone.utc) if d.tzinfo is None else d
    except (ValueError, AttributeError): return None

def private_json(path, value):
    """Exclusive file creation; never overwrite or follow a destination symlink."""
    path = Path(path).expanduser().absolute()
    if not path.parent.is_dir(): raise SafeError('Output parent must already exist; choose a private local folder.')
    try:
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, 'w') as f: json.dump(value, f, indent=2); f.write('\n')
    except FileExistsError: raise SafeError('Output already exists; choose a new filename.')

def read_json(path):
    try:
        with open(Path(path).expanduser()) as f: return json.load(f)
    except (ValueError, OSError): raise SafeError('Cannot read a required JSON file; check its path and syntax.')

COMMON = {'kind','model'}
FIELDS = {
    'subscription': {'email','organization_id'},
    'api': {'key_env','keychain_service','keychain_account'},
    'bedrock': {'aws_profile','region','account_id','principal_arn'},
    'foundry': {'resource','subscription_id','tenant_id','azure_account','key_env','keychain_service','keychain_account'},
}
REQUIRED = {
    'subscription': {'email','organization_id'},
    'api': set(),
    'bedrock': {'aws_profile','region','account_id','principal_arn'},
    'foundry': {'resource','subscription_id','tenant_id','azure_account'},
}

def validate_profile(p):
    if not isinstance(p,dict) or p.get('kind') not in FIELDS: raise SafeError('Unknown access kind.')
    kind=p['kind']
    if set(p)-(COMMON|FIELDS[kind]): raise SafeError('Unsupported profile fields. Store credential references, never literal secrets.')
    for name in REQUIRED[kind]:
        if not isinstance(p.get(name),str) or not p[name].strip(): raise SafeError('Profile is missing required identity or routing fields.')
    for value in p.values():
        if not isinstance(value,str) or '\x00' in value or '\n' in value: raise SafeError('Profile values must be single-line strings.')
        if value.startswith('REPLACE_') or '<' in value: raise SafeError('Replace all example placeholders before use.')
    if 'model' in p and not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._:/\[\]-]*',p['model']): raise SafeError('Model must be an identifier, not an option or command.')
    if kind in ('api','foundry'):
        by_env='key_env' in p
        by_keychain='keychain_service' in p and 'keychain_account' in p
        if by_env == by_keychain: raise SafeError('Choose exactly one key reference: key_env OR keychain_service plus keychain_account.')
        if by_env and not re.fullmatch(r'[A-Z_][A-Z0-9_]*',p['key_env']): raise SafeError('Invalid environment variable name.')
        if not by_keychain and ({'keychain_service','keychain_account'} & set(p)): raise SafeError('Incomplete Keychain reference.')
    if kind=='bedrock':
        if not re.fullmatch(r'\d{12}',p['account_id']): raise SafeError('AWS account_id must contain 12 digits.')
        if f":{p['account_id']}:" not in p['principal_arn']: raise SafeError('Principal ARN does not belong to expected AWS account.')
    if kind=='foundry' and not re.fullmatch(r'[a-zA-Z0-9-]+',p['resource']): raise SafeError('Foundry resource must be a resource name, not a URL.')
    return p

def routing_key(key):
    return key.startswith(('ANTHROPIC_', 'CLAUDE_CODE_USE_', 'CLAUDE_CODE_OAUTH_', 'AWS_', 'AZURE_')) or key in {'CLAUDE_CODE_API_KEY','CLAUDE_CODE_SKIP_BEDROCK_AUTH','CLAUDE_CODE_SKIP_FOUNDRY_AUTH','CLAUDE_CODE_SKIP_VERTEX_AUTH','DISABLE_PROMPT_CACHING'} or key.startswith('DISABLE_PROMPT_CACHING_')

def child_environment(source,p):
    # Store locations survive; switching them would make existing sessions disappear.
    keep={'AWS_CONFIG_FILE','AWS_SHARED_CREDENTIALS_FILE','AZURE_CONFIG_DIR'} if p['kind'] in ('bedrock','foundry') else set()
    env={k:v for k,v in source.items() if not routing_key(k) or k in keep}
    if p['kind']=='bedrock': env.update(CLAUDE_CODE_USE_BEDROCK='1',AWS_PROFILE=p['aws_profile'],AWS_REGION=p['region'],AWS_DEFAULT_REGION=p['region'])
    if p['kind']=='foundry': env.update(CLAUDE_CODE_USE_FOUNDRY='1',ANTHROPIC_FOUNDRY_RESOURCE=p['resource'])
    return env

def settings_paths(project,env):
    home=Path(env.get('HOME',str(Path.home())))
    store=Path(env.get('CLAUDE_CONFIG_DIR',str(home/'.claude'))).expanduser()
    if not store.is_absolute(): raise SafeError('CLAUDE_CONFIG_DIR must be absolute so settings and sessions resolve consistently.')
    paths=[store/'settings.json', store/'settings.local.json', store/'managed-settings.json']
    for folder in [project,*project.parents]:
        paths.extend([folder/'.claude/settings.json',folder/'.claude/settings.local.json'])
    if sys.platform=='darwin': paths.append(Path('/Library/Application Support/ClaudeCode/managed-settings.json'))
    else: paths.append(Path('/etc/claude-code/managed-settings.json'))
    return list(dict.fromkeys(paths))

def settings_conflicts(paths):
    found=[]
    for path in paths:
        if not path.exists(): continue
        data=read_json(path)
        if not isinstance(data,dict): raise SafeError('Settings object has unsupported structure.')
        for key in ('apiKeyHelper','model','forceLoginMethod','forceLoginOrgUUID','awsAuthRefresh','awsCredentialExport'):
            if key in data: found.append({'file':str(path),'key':key})
        env=data.get('env',{})
        if not isinstance(env,dict): raise SafeError('Settings env has unsupported structure.')
        for key in env:
            if routing_key(key) or key=='CLAUDE_CONFIG_DIR': found.append({'file':str(path),'key':'env.'+key})
    return found

def run_json(args,env,cwd):
    try: result=subprocess.run(args,env=env,cwd=cwd,capture_output=True,text=True,timeout=35,check=False)
    except (OSError,subprocess.TimeoutExpired): raise SafeError('Identity check unavailable or timed out; no fallback attempted.')
    if result.returncode: raise SafeError('Identity check failed. Inspect provider login separately; no fallback attempted.')
    try: return json.loads(result.stdout)
    except ValueError: raise SafeError('Identity output schema is unsupported; inspect official authentication status manually.')

def check_subscription(result,p):
    if not isinstance(result,dict) or result.get('loggedIn') is not True or result.get('authMethod')!='claude.ai':
        raise SafeError('Subscription OAuth login not confirmed. Use the official login flow, then retry.')
    if not isinstance(result.get('email'),str) or result['email'].casefold()!=p['email'].casefold() or result.get('orgId')!=p['organization_id']:
        raise SafeError('Subscription account or organisation does not match, or orgId is unavailable. Do not bypass this check.')

def verify_identity(p,env,project):
    if p['kind']=='bedrock':
        r=run_json(['aws','sts','get-caller-identity','--profile',p['aws_profile'],'--region',p['region'],'--output','json','--no-cli-pager'],env,project)
        if not isinstance(r,dict) or r.get('Account')!=p['account_id'] or r.get('Arn')!=p['principal_arn']: raise SafeError('AWS account or principal mismatch; stopped.')
    elif p['kind']=='foundry':
        # Verify default too: an explicit-subscription read alone does not prove SDK identity.
        r=run_json(['az','account','show','--output','json'],env,project)
        if not isinstance(r,dict) or r.get('id')!=p['subscription_id'] or r.get('tenantId')!=p['tenant_id'] or not isinstance(r.get('user'),dict) or not isinstance(r['user'].get('name'),str) or r['user']['name'].casefold()!=p['azure_account'].casefold(): raise SafeError('Azure default account, tenant or subscription mismatch; stopped without changing it.')
    elif p['kind']=='subscription': check_subscription(run_json(['claude','auth','status','--json'],env,project),p)

def load_key(p,source):
    if 'key_env' in p: value=source.get(p['key_env'],'')
    else:
        if sys.platform!='darwin': raise SafeError('Keychain credential source requires macOS. Use an environment reference on Linux.')
        try:
            result=subprocess.run(['security','find-generic-password','-s',p['keychain_service'],'-a',p['keychain_account'],'-w'],capture_output=True,text=True,timeout=30)
        except (OSError,subprocess.TimeoutExpired): raise SafeError('Keychain lookup failed or needs user interaction.')
        value=result.stdout.strip() if result.returncode==0 else ''
    if not value or '\n' in value or '\x00' in value: raise SafeError('Referenced credential is missing or invalid; no secret was printed.')
    return value

def launch(args):
    if os.name=='nt': raise SafeError('CLI launch is supported on macOS/Linux only; use the Desktop guide on Windows.')
    config=read_json(args.config)
    if not isinstance(config,dict) or not isinstance(config.get('profiles'),dict) or config.get('version')!=1 or args.profile not in config.get('profiles',{}): raise SafeError('Unknown profile or config version.')
    p=validate_profile(config['profiles'][args.profile])
    project=Path(args.project).expanduser().resolve()
    if not project.is_dir(): raise SafeError('Original project directory is missing. Restore or locate it; do not silently re-anchor.')
    env=child_environment(os.environ,p)
    conflicts=settings_conflicts(settings_paths(project,env))
    command=['claude']
    if p.get('model'): command+=['--model',p['model']]
    if args.resume: command+=['--resume',args.resume]
    plan={'mode':'execute' if args.execute else 'preview','profile':args.profile,'kind':p['kind'],'project':str(project),
          'command':command,'credential_source':'reference only' if p['kind'] in ('api','foundry') else 'provider login',
          'conflicts':conflicts,'desktop':'unchanged: use the Desktop guide','identity':'pending until --execute',
          'history':'same config directory; no migration or session copy','environment':'routing variables replaced only in child; inherited non-routing tools/hooks retain their existing configuration'}
    print(json.dumps(plan,indent=2))
    if conflicts: raise SafeError('Conflicting settings require review before launching. No settings were changed.')
    if not args.execute: return
    if not args.confirm_idle: raise SafeError('Confirm no task is running before switching: --confirm-idle. The tool cannot prove Desktop is idle.')
    if p['kind'] in ('bedrock','foundry') and not args.reviewed_provider_policy: raise SafeError('Read your provider/profile guardrails first, then pass --reviewed-provider-policy.')
    if not shutil.which('claude'): raise SafeError('Claude CLI not found. Install from the official source or use Desktop guidance.')
    verify_identity(p,env,project)
    if p['kind'] in ('api','foundry'):
        key=load_key(p,os.environ)
        if 'key_env' in p: env.pop(p['key_env'],None)
        env['ANTHROPIC_API_KEY' if p['kind']=='api' else 'ANTHROPIC_FOUNDRY_API_KEY']=key
    # Do not pass arbitrary extra CLI flags, provider fallbacks or shell commands.
    print('Launching terminal Claude. Verify its provider/model before submitting work. Desktop remains unchanged.',flush=True)
    raise SystemExit(subprocess.call(command,cwd=project,env=env))

def iter_files(paths,suffix=None):
    found=set()
    for raw in paths:
        p=Path(raw).expanduser().absolute()
        if p.is_symlink() or not p.exists(): raise SafeError('Source is missing or a symlink. Select the verified original path explicitly.')
        if p.is_file(): candidates=[p]
        elif p.is_dir():
            candidates=[]
            for folder,dirs,files in os.walk(p,followlinks=False):
                dirs[:]=sorted(d for d in dirs if not (Path(folder)/d).is_symlink())
                candidates.extend(Path(folder)/n for n in sorted(files) if not (Path(folder)/n).is_symlink())
        else: raise SafeError('Only regular files/directories are supported.')
        for f in candidates:
            if f.is_file() and (suffix is None or f.suffix==suffix): found.add(f)
    return sorted(found)

def digest(path,limit=None):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        while limit is None or limit>0:
            chunk=f.read(min(1024*1024,limit) if limit is not None else 1024*1024)
            if not chunk: break
            h.update(chunk)
            if limit is not None: limit-=len(chunk)
    return h.hexdigest()

def snapshot(paths):
    records=[]
    for p in iter_files(paths):
        before=p.stat(); sha=digest(p); after=p.stat()
        if (before.st_size,before.st_mtime_ns)!=(after.st_size,after.st_mtime_ns): raise SafeError('A source changed during inventory. Wait for idle and retry; no stable snapshot claimed.')
        records.append({'path':str(p),'bytes':before.st_size,'sha256':sha})
    return {'version':1,'created':datetime.now(timezone.utc).isoformat(),'roots':[str(Path(p).expanduser().absolute()) for p in paths],
            'meaning':'metadata and hashes only; NOT a backup, transcript transfer, or proof of semantic continuity; symlinks below roots excluded', 'files':records}

def compare_snapshot(baseline):
    if baseline.get('version')!=1: raise SafeError('Unsupported manifest version.')
    counts={k:0 for k in ('unchanged','appended','changed','missing','new')}; results=[]
    known=set()
    for r in baseline['files']:
        p=Path(r['path']); known.add(p)
        if not p.exists(): state='missing'
        elif p.is_symlink() or not p.is_file(): state='changed'
        elif digest(p)==r['sha256']: state='unchanged'
        elif p.stat().st_size>r['bytes'] and digest(p,r['bytes'])==r['sha256']: state='appended'
        else: state='changed'
        counts[state]+=1; results.append({'path':str(p),'state':state})
    for root in baseline['roots']:
        if Path(root).exists() and not Path(root).is_symlink():
            for p in iter_files([root]):
                if p not in known: counts['new']+=1; known.add(p); results.append({'path':str(p),'state':'new'})
    return {'counts':counts,'files':results,'meaning':'Byte comparison only. Appended history still needs resume/context verification.'}

def handoff(args):
    project=Path(args.project).expanduser().resolve()
    if not project.is_dir(): raise SafeError('Original project folder missing; no alternative directory will be substituted.')
    refs=iter_files(args.sources)
    output={'version':1,'title':args.title,'project':str(project),'source_references':[str(p) for p in refs],
            'goal':'FILL IN: current objective','last_verified_state':'FILL IN: evidence and date',
            'decisions':[],'pending_actions':[],'constraints':[],'memory_and_rules':[],
            'tools_and_auth_references':[], 'relationships':{'original_session_id':'FILL IN','parent_id':None,'project_group':'FILL IN','archived':False},
            'validation':{'original_files_unchanged':'not checked','resumed_in_desktop':'not checked','context_understood':'not checked'},
            'notice':'Keep private. Add credential LOCATION references only, never values. This handoff does not automatically import native sessions.'}
    private_json(args.output,output)
    print('Created a small reference handoff. Fill its context fields before continuing in the destination app.')

def valid_counter(value):
    return isinstance(value,int) and not isinstance(value,bool) and value>=0

def number(value):
    return value if valid_counter(value) else 0

def valid_usage(u,kind):
    required=('input_tokens','output_tokens') if kind=='claude' else ('input_tokens','cached_input_tokens','output_tokens')
    optional=('cache_read_input_tokens','cache_creation_input_tokens') if kind=='claude' else ()
    return all(valid_counter(u.get(k)) for k in required) and all(valid_counter(u[k]) for k in optional if k in u)

def usage_report(paths,kind,since):
    files=iter_files(paths,'.jsonl'); records={}; malformed=0; skipped=0; resets=0; baselines=0; schema_skips=0
    for file in files:
        prev=None
        with open(file,errors='replace') as f:
            for line_no,line in enumerate(f,1):
                try: row=json.loads(line)
                except ValueError: malformed+=1; continue
                if not isinstance(row,dict): malformed+=1; continue
                stamp=parse_time(row.get('timestamp'))
                if kind=='claude':
                    msg=row.get('message')
                    if row.get('type')!='assistant' or not isinstance(msg,dict) or not isinstance(msg.get('usage'),dict) or not msg.get('id'): continue
                    if not stamp or stamp<since: skipped+=1; continue
                    u=msg['usage']
                    if not valid_usage(u,kind): schema_skips+=1; continue
                    key=str(msg['id'])
                    val={'input':number(u.get('input_tokens'))+number(u.get('cache_read_input_tokens'))+number(u.get('cache_creation_input_tokens')),
                         'cache':number(u.get('cache_read_input_tokens')),'output':number(u.get('output_tokens')),
                         'model':str(msg.get('model','unknown')),'day':stamp.date().isoformat()}
                    if key in records:
                        for field in ('input','cache','output'): val[field]=max(val[field],records[key][field])
                    records[key]=val
                else:
                    payload=row.get('payload',{})
                    if not isinstance(payload,dict) or payload.get('type')!='token_count': continue
                    info=payload.get('info') or {}
                    if not isinstance(info,dict): continue
                    u=info.get('total_token_usage')
                    if not isinstance(u,dict) or not valid_usage(u,kind) or not stamp: schema_skips+=1; continue
                    cur=(number(u.get('input_tokens')),number(u.get('cached_input_tokens')),number(u.get('output_tokens')))
                    old=prev; prev=cur
                    if old is None: baselines+=1; continue
                    if any(c<b for c,b in zip(cur,old)): resets+=1; continue
                    if not stamp or stamp<since or cur==old: continue
                    key=(str(file),line_no)
                    records[key]={'input':cur[0]-old[0],'cache':cur[1]-old[1],'output':cur[2]-old[2], 'model':'unattributed-codex','day':stamp.date().isoformat()}
    totals=Counter(); models=defaultdict(Counter); days=defaultdict(Counter)
    for r in records.values():
        for k in ('input','cache','output'): totals[k]+=r[k]; models[r['model']][k]+=r[k]; days[r['day']][k]+=r[k]
    rate=round(100*totals['cache']/totals['input'],2) if totals['input'] else None
    total=totals['input']+totals['output']
    flags=[]
    if rate is not None and rate<85: flags.append('Cache hit rate below 85%; inspect repeated model/tool/instruction changes before changing TTL.')
    if rate is not None and rate>100: flags.append('Cache counters inconsistent; treat this report as incomplete.')
    premium={name:round(100*(v['input']+v['output'])/total,2) for name,v in models.items() if total and any(x in name.lower() for x in ('opus','fable'))}
    # A request can be part of a multi-request prompt; this is a lower-bound review signal.
    big=sum(1 for r in records.values() if total and (r['input']+r['output'])/total>.02)
    if big: flags.append(f'{big} recorded request/delta entries exceed 2% of observed tokens. These are not complete user-prompt totals.')
    if premium: flags.append('Review premium-model shares against the work performed; high cost cannot be inferred from token share alone.')
    return {'version':1,'source':kind,'since':since.isoformat(),'status':('partial-data' if malformed or schema_skips or resets else 'observed-data') if records else 'insufficient-data',
            'files_read':len(files),'requests':len(records) if kind=='claude' else None,'usage_delta_entries':len(records) if kind=='codex' else None,
            'input_tokens':totals['input'],'cached_input_tokens':totals['cache'],'output_tokens':totals['output'],'cache_hit_percent':rate,
            'model_tokens':dict(models),'daily_tokens':dict(days),'premium_model_token_percent':premium,'large_entries':big,
            'subagent_usage':'not reliably attributable by these adapters; inspect native session report',
            'single_prompt_totals':'not reconstructed; request/delta flags are a partial signal',
            'malformed_lines':malformed,'skipped_usage_records':schema_skips,'skipped_claude_requests':skipped,'codex_initial_baselines_excluded':baselines,'counter_resets_excluded':resets,
            'flags':flags,'billing':'No dollar estimate. Compare provider console period, organisation, credits and cap separately.',
            'limits':['Local schema adapters may miss usage; forks can repeat cumulative history. Select non-overlapping source files.',
                      'Claude deduplicates message IDs; Codex excludes the initial cumulative baseline and decreases.',
                      'Missing timestamps or unknown schemas are not proof of zero use. Includes no transcript contents.']}

def install_skill(target,apply):
    target=Path(target).expanduser().absolute(); dest=target/'ai-workbench'
    if dest.exists() or dest.is_symlink(): raise SafeError('Skill destination already exists. Review it; this command never overwrites.')
    if apply:
        target.mkdir(parents=True,exist_ok=True)
        # Copy this small self-contained skill package, never an app store or repository.
        shutil.copytree(SKILL,dest,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
    return {'action':'installed' if apply else 'preview','source':str(SKILL),'destination':str(dest),'scope':'one skill with its own docs, templates and script; no hooks, MCPs or credentials'}

def doctor():
    total,used,free=shutil.disk_usage(Path.home())
    return {'kit_version':VERSION,'python':sys.version.split()[0],'platform':sys.platform,
            'executables':{x:bool(shutil.which(x)) for x in ('claude','codex','aws','az')},
            'disk_free_gib':round(free/1024**3,1),'disk_warning':free<10*1024**3,
            'inherited_routing_variable_names':sorted(k for k in os.environ if routing_key(k)),
            'custom_claude_store':bool(os.environ.get('CLAUDE_CONFIG_DIR')),
            'checks_not_done':['login/plan/billing','Desktop mode','session visibility','model availability'],
            'notice':'Offline inventory only. No app was installed, started, updated, or reconfigured.'}

def codex_review(args):
    import tomllib
    path=Path(args.config).expanduser()
    try:
        with open(path,'rb') as f: cfg=tomllib.load(f)
    except (OSError,ValueError): raise SafeError('Cannot read Codex TOML; no changes made.')
    fields=('model','model_reasoning_effort','service_tier','model_provider','profile')
    safe={k:cfg[k] for k in fields if isinstance(cfg.get(k),(str,int,bool))}
    print(json.dumps({'settings':safe,'profile_names':list(cfg.get('profiles',{})), 'changed':False,
       'recommendations':['Choose a currently available economical coding model for new routine work.',
                          'Use medium effort for routine work; increase it when task complexity warrants it.',
                          'Inspect the app speed/service-tier label and price before opting into premium speed.',
                          'Preserve provider, authentication, safety permissions and existing sessions.',
                          'Native caching is automatic; do not add keepalive prompts or a caching proxy.'],
       'limitations':'CLI TOML does not prove the effective Desktop model or billing route.'},indent=2))

def parser():
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('--version',action='version',version=VERSION)
    sub=p.add_subparsers(dest='command',required=True)
    sub.add_parser('doctor',help='Offline prerequisite inventory; changes nothing')
    q=sub.add_parser('init',help='Create a profile template, never overwrite'); q.add_argument('--output',required=True)
    q=sub.add_parser('launch',help='Preview a terminal wrapper; Desktop is unchanged')
    q.add_argument('profile'); q.add_argument('--config',required=True); q.add_argument('--project',required=True); q.add_argument('--resume')
    q.add_argument('--execute',action='store_true'); q.add_argument('--confirm-idle',action='store_true'); q.add_argument('--reviewed-provider-policy',action='store_true')
    q=sub.add_parser('snapshot',help='Save hashes and path references, not copies'); q.add_argument('paths',nargs='+'); q.add_argument('--output',required=True)
    q=sub.add_parser('compare',help='Compare an earlier manifest'); q.add_argument('manifest'); q.add_argument('--output')
    q=sub.add_parser('handoff',help='Create a context handoff skeleton with references'); q.add_argument('--project',required=True); q.add_argument('--title',required=True); q.add_argument('--sources',nargs='+',required=True); q.add_argument('--output',required=True)
    q=sub.add_parser('usage',help='Read selected local JSONL metadata; never call a model'); q.add_argument('paths',nargs='+'); q.add_argument('--source',choices=['claude','codex'],required=True); q.add_argument('--days',type=int,default=7); q.add_argument('--output',required=True)
    q=sub.add_parser('install-skill',help='Preview installation of the self-contained AI skill'); q.add_argument('--target',required=True); q.add_argument('--apply',action='store_true')
    q=sub.add_parser('codex-review',help='Read selected nonsecret settings from a Codex TOML'); q.add_argument('--config',required=True)
    return p

def main():
    args=parser().parse_args()
    try:
        if args.command=='doctor': print(json.dumps(doctor(),indent=2))
        elif args.command=='init': private_json(args.output,read_json(SKILL/'assets/profiles.example.json')); print('Created private profile template. Replace placeholders for only the routes you use.')
        elif args.command=='launch': launch(args)
        elif args.command=='snapshot': private_json(args.output,snapshot(args.paths)); print('Created reference manifest; no source files copied.')
        elif args.command=='compare':
            report=compare_snapshot(read_json(args.manifest))
            if args.output: private_json(args.output,report)
            else: print(json.dumps(report,indent=2))
            if report['counts']['changed'] or report['counts']['missing']: return 3
        elif args.command=='handoff': handoff(args)
        elif args.command=='usage':
            if not 1<=args.days<=366: raise SafeError('days must be between 1 and 366.')
            report=usage_report(args.paths,args.source,datetime.now(timezone.utc)-timedelta(days=args.days)); private_json(args.output,report)
            print('Saved private token metadata. Provider billing and native session review are still required.')
        elif args.command=='install-skill': print(json.dumps(install_skill(args.target,args.apply),indent=2))
        elif args.command=='codex-review': codex_review(args)
        return 0
    except (SafeError,OSError) as e:
        # Avoid raw subprocess outputs; exceptions from app/auth payloads are never emitted.
        print('Stopped: '+(str(e) if isinstance(e,SafeError) else 'Local filesystem operation failed; check paths and permissions.'),file=sys.stderr)
        return 2

if __name__=='__main__': raise SystemExit(main())
