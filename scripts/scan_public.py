"""Scan publishable or staged files without printing suspected secret values."""
import argparse
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
RULES = {
    'private-key': re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----'),
    'github-token': re.compile(r'\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})\b'),
    'api-key': re.compile(r'\bsk-(?:proj-)?[A-Za-z0-9_-]{24,}\b'),
    'aws-access-key': re.compile(r'\bAKIA[0-9A-Z]{16}\b'),
    'machine-path': re.compile(r'(?i)(?:[A-Z]:[\\/](?:Users|3am|Data)[\\/]|/(?:Users|home)/[^\s\"\'<>]+)'),
    'personal-cachebuster': re.compile(r'\+codex\.\d{8,}'),
}
EMAIL = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b')
SAFE_DOMAINS = {'example.com', 'example.org', 'example.net'}
FORBIDDEN_SUFFIXES = {'.pem', '.key', '.p12', '.pfx'}


def findings(name, data):
    path = Path(name)
    result = []
    if path.suffix.lower() in FORBIDDEN_SUFFIXES or path.name in {'.env', 'auth.json', 'config.toml'}:
        result.append('private-file')
    if any(part in {'learning', '.codex', '.claude', '.superlearn'} for part in path.parts):
        result.append('local-state')
    try:
        content = data.decode('utf-8-sig')
    except UnicodeDecodeError:
        return result + ['unexpected-binary']
    for rule, pattern in RULES.items():
        if pattern.search(content):
            result.append(rule)
    if any(match.group().rsplit('@', 1)[1].lower() not in SAFE_DOMAINS
           for match in EMAIL.finditer(content)):
        result.append('email-address')
    return result


def git(*args):
    return subprocess.check_output(['git', '-c', 'core.quotepath=false', *args], cwd=ROOT)


def scan(staged=False):
    args = ['ls-files', '-z', '--cached']
    if not staged:
        args.extend(['--others', '--exclude-standard'])
    names = sorted(set(git(*args).decode('utf-8').split('\0')) - {''})
    failures = []
    for name in names:
        path = ROOT / name
        if not staged and not path.exists():
            continue
        data = git('show', ':' + name) if staged else path.read_bytes()
        failures.extend((name, rule) for rule in findings(name, data))
    return len(names), failures


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--staged', action='store_true', help='Read the actual index bytes')
    args = parser.parse_args()
    count, failures = scan(args.staged)
    for name, rule in failures:
        print(f'{name}: {rule}', file=sys.stderr)
    if failures:
        print('Public-content scan failed; matched values are intentionally not displayed.', file=sys.stderr)
        return 1
    print(f'Public-content scan passed for {count} files (common-pattern scan, not an exhaustive guarantee).')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
