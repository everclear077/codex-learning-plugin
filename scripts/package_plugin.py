"""Create a deterministic plugin-only ZIP using public-content checks."""
import json
from pathlib import Path
import sys
import zipfile

from scan_public import findings

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / 'plugins/core-learning'


def package(output_dir=None):
    manifest = json.loads((PLUGIN / '.codex-plugin/plugin.json').read_text(encoding='utf-8'))
    output_dir = Path(output_dir) if output_dir is not None else ROOT / 'dist'
    output_dir.mkdir(parents=True, exist_ok=True)
    output = output_dir / f"core-learning-{manifest['version']}.zip"
    files = []
    for file in sorted(PLUGIN.rglob('*')):
        if not file.is_file() or '__pycache__' in file.parts or file.suffix == '.pyc':
            continue
        relative = file.relative_to(PLUGIN).as_posix()
        if file.is_symlink() or (file.suffix not in {'.md', '.py', '.json', '.yaml'} and relative not in {'LICENSE', 'assets/icon.svg'}):
            raise ValueError(f'Unexpected package file: {relative}')
        data = file.read_bytes()
        problems = findings(relative, data)
        if problems:
            raise ValueError(f'Unsafe package file: {relative} ({", ".join(problems)})')
        files.append((relative, data))
    names = {name for name, _ in files}
    required = {'.codex-plugin/plugin.json', 'skills/learn-core/SKILL.md', 'LICENSE'}
    if not required.issubset(names):
        raise ValueError('Missing required package files')
    with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED) as archive:
        for name, data in files:
            info = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, data)
    with zipfile.ZipFile(output) as archive:
        if archive.testzip() is not None or set(archive.namelist()) != names:
            raise ValueError('Archive verification failed')
    print(f'Packaged {len(files)} files: {output.name}')
    return output


if __name__ == '__main__':
    try:
        package()
    except (ValueError, OSError) as error:
        print(f'Packaging failed: {error}', file=sys.stderr)
        raise SystemExit(1)
