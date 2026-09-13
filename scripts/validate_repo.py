"""Validate this repository's portable distribution contract and local links."""
import ast
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

import yaml

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / 'plugins/core-learning'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def internal(base, value, boundary):
    require(isinstance(value, str) and value.startswith('./'), 'Expected ./ relative path')
    path = (base / value).resolve()
    require(path.is_relative_to(boundary.resolve()), 'Path escapes its distribution root')
    require(path.exists(), f'Missing path: {value}')
    return path


def validate():
    market = json.loads((ROOT / '.agents/plugins/marketplace.json').read_text(encoding='utf-8'))
    require(market['name'] == 'codex-learning', 'Unexpected marketplace ID')
    require(len(market['plugins']) == 1, 'Expected one published plugin')
    entry = market['plugins'][0]
    require(entry['name'] == 'core-learning', 'Marketplace/plugin mismatch')
    require(entry['source']['source'] == 'local', 'Expected repository-local plugin')
    require(internal(ROOT, entry['source']['path'], ROOT) == PLUGIN.resolve(), 'Wrong plugin path')
    require(entry['policy'] == {'installation': 'AVAILABLE', 'authentication': 'ON_INSTALL'}, 'Unexpected policy')
    require(entry['category'] == 'Productivity', 'Missing category')
    manifest = json.loads((PLUGIN / '.codex-plugin/plugin.json').read_text(encoding='utf-8'))
    require(manifest['name'] == PLUGIN.name, 'Manifest/folder mismatch')
    require(bool(re.fullmatch(r'\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?', manifest['version'])), 'Use public semver without local build suffix')
    require(manifest['license'] == 'MIT', 'License mismatch')
    require(manifest['author']['name'].strip(), 'Missing author')
    require(manifest['description'].strip(), 'Missing description')
    require(not any(key in manifest for key in ('hooks', 'apps', 'mcpServers')), 'Unexpected runtime capability')
    skills = internal(PLUGIN, manifest['skills'], PLUGIN)
    interface = manifest['interface']
    require(interface['displayName'] == '学习', 'Unexpected display name')
    require(interface['capabilities'] == [], 'Unexpected capability claims')
    require(1 <= len(interface['defaultPrompt']) <= 3, 'Need 1–3 prompts')
    require(all(isinstance(p, str) and 0 < len(p) <= 128 for p in interface['defaultPrompt']), 'Invalid prompt')
    for key in ('homepage', 'repository'):
        require(urlsplit(manifest[key]).scheme == 'https', f'{key} must use HTTPS')
    skill = skills / 'learn-core'
    body = (skill / 'SKILL.md').read_text(encoding='utf-8')
    require(body.startswith('---\n'), 'Missing skill YAML frontmatter')
    frontmatter = yaml.safe_load(body.split('---', 2)[1])
    require(frontmatter['name'] == skill.name, 'Skill/folder mismatch')
    require(bool(frontmatter['description'].strip()), 'Missing skill description')
    ui = yaml.safe_load((skill / 'agents/openai.yaml').read_text(encoding='utf-8'))
    require('$learn-core' in ui['interface']['default_prompt'], 'Wrong skill invocation')
    require(25 <= len(ui['interface']['short_description']) <= 64, 'Invalid skill subtitle length')
    require((ROOT / 'LICENSE').read_bytes() == (PLUGIN / 'LICENSE').read_bytes(), 'Plugin license differs')
    required = ['README.md', 'README.en.md', 'AGENTS.md', 'CLAUDE.md', 'CONTRIBUTING.md',
                'SECURITY.md', 'PRIVACY.md', 'CHANGELOG.md', '.gitignore', '.github/workflows/ci.yml']
    for name in required:
        require((ROOT / name).is_file(), f'Missing {name}')
    checks = 0
    for path in ROOT.rglob('*'):
        relative = path.relative_to(ROOT)
        if any(p in {'.git', '.venv', '__pycache__', 'dist', 'learning'} for p in relative.parts) or not path.is_file():
            continue
        if path.suffix == '.py':
            ast.parse(path.read_text(encoding='utf-8'), feature_version=(3, 10))
        if path.suffix in {'.yaml', '.yml'}:
            yaml.safe_load(path.read_text(encoding='utf-8'))
        if path.suffix != '.md':
            continue
        content = path.read_text(encoding='utf-8')
        require('[TODO:' not in content, f'Unfinished placeholder in {relative}')
        for link in re.findall(r'\]\(([^)]+)\)', content):
            if '://' in link or link.startswith('#'):
                continue
            target = (path.parent / unquote(link.split('#')[0])).resolve()
            boundary = PLUGIN if path.is_relative_to(PLUGIN) else ROOT
            require(target.is_relative_to(boundary.resolve()) and target.is_file(), f'Broken/local escape link in {relative}: {link}')
            checks += 1
    print(f'Repository contract, Python/YAML syntax and {checks} local links passed.')


if __name__ == '__main__':
    try:
        validate()
    except (ValueError, KeyError, OSError, SyntaxError, yaml.YAMLError) as error:
        print(f'Validation failed: {error}', file=sys.stderr)
        raise SystemExit(1)
