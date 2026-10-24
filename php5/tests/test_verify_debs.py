"""Exercise release inventory failures using temporary synthetic .deb files."""
# SPDX-License-Identifier: MIT
import json
from pathlib import Path
import runpy
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
VERIFY = runpy.run_path(str(ROOT / 'verify-debs.py'))['verify']


@unittest.skipUnless(shutil.which('dpkg-deb'), 'requires dpkg-deb')
class VerifyDebsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.work = Path(self.temp.name)
        self.assets = self.work / 'assets'
        self.assets.mkdir()
        with (ROOT / 'release-plan.json').open(encoding='utf-8') as stream:
            self.plan = json.load(stream)
        for item in self.plan['packages']:
            self.build(item, self.plan['package_version'])

    def tearDown(self):
        self.temp.cleanup()

    def build(self, item, version):
        package = self.work / item['name']
        control = package / 'DEBIAN'
        control.mkdir(parents=True, exist_ok=True)
        (control / 'control').write_text(
            'Package: {0}\nVersion: {1}\nArchitecture: {2}\n'
            'Maintainer: Test Fixture <fixture@example.invalid>\n'
            'Description: Temporary metadata verification fixture\n'.format(
                item['name'], version, item['architecture']))
        payload = package / 'usr/share/release-verifier-fixture'
        payload.mkdir(parents=True, exist_ok=True)
        (payload / 'fixture.txt').write_text('synthetic fixture, not a PHP binary\n')
        subprocess.check_call(['dpkg-deb', '--build', str(package),
                               str(self.assets / item['filename'])],
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def test_complete_matching_inventory(self):
        rows = VERIFY(self.assets, self.plan)
        self.assertEqual(len(rows), 12)
        self.assertTrue(all(len(row['sha256']) == 64 and row['size_bytes'] > 0
                            for row in rows))

    def test_mixed_package_version_is_rejected(self):
        self.build(self.plan['packages'][0], '5.6.40+dfsg-0+deb8u12')
        with self.assertRaises(ValueError):
            VERIFY(self.assets, self.plan)

    def test_missing_binary_is_rejected(self):
        (self.assets / self.plan['packages'][0]['filename']).unlink()
        with self.assertRaises(ValueError):
            VERIFY(self.assets, self.plan)

    def test_unselected_extra_binary_is_rejected(self):
        (self.assets / 'unselected.deb').write_bytes(b'not a package')
        with self.assertRaises(ValueError):
            VERIFY(self.assets, self.plan)


if __name__ == '__main__':
    unittest.main()
