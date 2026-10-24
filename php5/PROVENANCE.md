# Source provenance

## Base

Debian Jessie source package: `php5 5.6.40+dfsg-0+deb8u12`.

Download these files from
<https://archive.debian.org/debian-security/pool/updates/main/p/php5/>:

- `php5_5.6.40+dfsg.orig.tar.gz`
- `php5_5.6.40+dfsg-0+deb8u12.debian.tar.xz`
- `php5_5.6.40+dfsg-0+deb8u12.dsc`

The original Debian rules, control file, and inherited 79-patch series are retained.
The local additions are the three vendor patches, their series entries, and a
local changelog entry.

## Vendor backports

DEB.SURY.ORG source package:
`php5.6 5.6.40-105+0~20261022.135+debian11~1.gbp37a17e`.

The exact packaging archive is
[`php5.6_5.6.40-105+0~20261022.135+debian11~1.gbp37a17e.debian.tar.xz`](https://packages.sury.org/php/pool/main/p/php5.6/php5.6_5.6.40-105+0~20261022.135+debian11~1.gbp37a17e.debian.tar.xz).

Its packaging identifies the
[Debian PHP team repository](https://salsa.debian.org/php-team/php.git), branch
`debian/main/5.6`. The runtime upstream is [php/php-src](https://github.com/php/php-src).
The three committed patches were extracted byte-for-byte from this archive;
their original author headers and commit references are retained.

## Integrity boundary

[inputs.sha256](inputs.sha256) pins all four input archives.
[patches.sha256](patches.sha256) pins the three extracted patch files.
The archive and patch hashes were checked again while preparing this repository
on 24 October 2026, independently of the original build host.

The original preparation did **not** authenticate the Debian `.dsc` signature:
the required signing key was unavailable. A matching SHA-256 establishes equality
with the recorded bytes, not independent authentication of the publisher.
The source preparation helper explicitly skips `.dsc` signature checking after
checking the pinned file hashes. It does not alter APT trust settings.

The source preparation helper reconstructs the recorded runtime patch set. It
does not recover the exact original local changelog or the original build
environment. Its distinct package revision ends in `+rebuild1`. It must not be
presented as the exact corresponding source of the previously deployed binaries,
or as proof of a bit-for-bit reproducible build.

The complete corresponding source package for the original `+local20261023.1` binaries is included in the [versioned release](https://github.com/tomasgal/legacy-arm-builds/releases/tag/php5-jessie-armhf-local20261023.1). It consists of the local `.dsc`, the unchanged upstream `.orig.tar.gz`, and the local `.debian.tar.xz`. Its original local changelog was preserved, with SHA-256 `aa947af90df0ee19c4b3f7917eddc3847646dee368fc5241b8749076b79760c0`.

Unpacking this source package reproduces all 18,008 regular-file/symlink entries of the recovered pre-build tree by content, link target, and executable flag, excluding quilt bookkeeping. Twenty selected patched-runtime and packaging files also match the completed native build tree. See [original-build.json](original-build.json) and [SHA256SUMS](SHA256SUMS) for the recorded evidence. The local source descriptor is unsigned.
