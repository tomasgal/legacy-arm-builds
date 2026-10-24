#!/usr/bin/env python3
"""Check the selected original-build binaries; does not install or upload them."""
# SPDX-License-Identifier: MIT
from __future__ import print_function

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys


def sha256(path):
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def verify(directory, plan):
    rows = []
    expected = set(item['filename'] for item in plan['packages'])
    actual = set(path.name for path in directory.glob('*.deb'))
    if actual != expected:
        raise ValueError('Binary file set differs; missing={0}; unexpected={1}'.format(
            sorted(expected - actual), sorted(actual - expected)))
    for item in plan['packages']:
        path = directory / item['filename']
        if not path.is_file() or path.is_symlink():
            raise ValueError('Not a regular, non-symlink package: ' + path.name)
        values = []
        for field in ('Package', 'Version', 'Architecture'):
            value = subprocess.check_output(['dpkg-deb', '-f', str(path), field])
            values.append(value.decode('utf-8').strip())
        target = [item['name'], plan['package_version'], item['architecture']]
        if values != target:
            raise ValueError('Metadata mismatch for {0}: {1!r}'.format(path.name, values))
        # Read the data archive as well as the control fields; emit no path list.
        subprocess.check_call(['dpkg-deb', '--contents', str(path)], stdout=subprocess.DEVNULL)
        rows.append({'filename': path.name, 'size_bytes': path.stat().st_size,
                     'sha256': sha256(path)})
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path)
    parser.add_argument('--write-checksums', action='store_true',
                        help='Create SHA256SUMS.debs; refuses to replace an existing file')
    args = parser.parse_args()
    plan_path = Path(__file__).resolve().with_name('release-plan.json')
    try:
        with plan_path.open('r', encoding='utf-8') as stream:
            plan = json.load(stream)
        directory = args.directory.resolve()
        if not directory.is_dir():
            raise ValueError('Artifact directory is not a directory')
        rows = verify(directory, plan)
        if args.write_checksums:
            destination = directory / 'SHA256SUMS.debs'
            # Exclusive creation prevents overwriting a prior inspection record.
            with destination.open('x', encoding='ascii') as stream:
                for item in rows:
                    stream.write('{sha256}  {filename}\n'.format(**item))
        print(json.dumps({'result': 'SELECTED_BINARIES_OK', 'packages': rows,
                          'release_ready': False,
                          'remaining': 'Corresponding source, privacy and license inspection'},
                         indent=2, sort_keys=True))
        return 0
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print('VERIFY_FAILED: ' + str(error), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
