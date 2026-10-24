# Validation record and limits

## Original build: reported execution evidence, 24 October 2026

The following results were reported from the native ARM build and test host.
They are a record of that execution, not an independent rerun from this checkout.

- Native Jessie armhf build returned exit code 0.
- All binary entries in the generated `.changes` passed their SHA-256 checks.
- The selected twelve packages passed metadata inspection and a dpkg dry run.
- CLI loaded the required extensions, including the existing external JSON/APCu
  packages, and passed selected JSON, APCu, GD, GMP, and Intl function checks.
- CLI allocation beyond an 8 MiB memory limit exited with status 1 and did not
  execute a registered shutdown callback.
- A separate loopback-only Apache/prefork instance loaded the new mod_php and
  extensions. Session continuity, a multipart PNG, a raw upload of 3,145,796 bytes,
  and an explicitly configured multipart part limit passed.
- The isolated Apache test observed worker termination/replacement after OOM,
  absence of the shutdown callback marker, and session continuity afterward.
- The selected twelve packages were installed at the exact local revision;
  existing PHP/Apache configurations were retained. Apache syntax, restart, and
  active status passed.

The external packages `php5-json 1.3.6-1` and `php5-apcu 4.0.7-1` were reused;
this project did not rebuild them. Their selected CLI/mod_php functions were
exercised, which does not constitute a general extension ABI guarantee.

An application upload and image normalization succeeded after installation.
Intermittent upload failures were also observed and later could not be reproduced.
Their cause was not established. A perceived upload speed improvement was not
benchmarked and is not attributed to the patches.

## Repository preparation

The four recorded source inputs were downloaded again and their SHA-256 values
matched. All three committed patches match both their recorded SHA-256 values
and their byte sequences inside the pinned vendor archive. The licenses were
copied from the pinned PHP and Debian source inputs.

The new public source-preparation helper was run end-to-end on 24 October 2026:
all four downloads matched their pinned hashes, all three patches matched the
vendor archive, and dpkg-source applied the resulting 82-entry Debian series
without fuzz. The prepared version was the separate `+rebuild1` revision. This
was source preparation on a separate Linux environment, not a second native
ARM build or a bit-for-bit match to the deployed packages.

The binary verifier passed four tests with temporary synthetic Debian packages:
a complete matching inventory was accepted; a missing binary, an unexpected
additional binary, and a mixed package version were rejected. Those synthetic
fixtures are not PHP builds and are not release assets. Run these helper tests:

```sh
python3 -m unittest discover -s php5/tests -p 'test_*.py' -v
```

## Original asset import and source export, 24 October 2026

- The original twelve binaries match their original native `.changes` SHA-256 entries. Package names, exact versions, architectures, and readable payload archives passed the existing verifier.
- The original source input hashes, three vendor patch hashes, and 82-entry series match the pinned records. The PHP license and Debian copyright inventory are retained verbatim.
- The complete source package was exported from a copy of the exact pre-build tree. Re-extraction matched all 18,008 regular-file/symlink entries by content, link target, and executable flag, excluding quilt bookkeeping.
- Twenty selected patched-runtime and packaging files match the completed native build tree. The original generic local changelog is unchanged.
- Binary control fields, payloads, compressed documentation, and source archives were inspected for operator-specific contact, host, network, repository, and deployment-path strings; no such matches were found. Required upstream attribution was retained.
- No runtime build, installation, or previously accepted runtime test was repeated for publication. The [manifest](original-build.json) records the scope and actual artifact hashes.

## Unverified areas

- The full PHP/Debian suite was skipped during the original build (`nocheck`).
- FPM request handling and the additional generated SAPIs/extensions were not
  independently accepted.
- A live package downgrade/rollback was not executed.
- Long-term reliability and arbitrary applications, inputs, devices, or
  distributions were not evaluated.

The public CLI smoke scripts are newly supplied helpers, not a claim that the
original test harness has been recovered. Run failure-path tests in isolation.
With the intended PHP 5.6 executable and its extension configuration available:

```sh
/absolute/path/to/php5 -d apc.enable_cli=1 -d opcache.enable_cli=0 php5/tests/cli-smoke.php
```

The following CLI-only test deliberately exhausts a small memory limit and
expects that PHP process to exit with status 1, without a shutdown callback:

```sh
sh php5/tests/oom-cli.sh /absolute/path/to/php5
```

These new PHP smoke helpers were not run as part of the publication audit. The recorded original tests above remain a separate evidence boundary.
