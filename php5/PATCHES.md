# Selected patch manifest

Base: `php5 5.6.40+dfsg-0+deb8u12`. Deployed local revision:
`5.6.40+dfsg-0+deb8u12+local20261023.1`.

| Patch | Purpose | Bytes |
| --- | --- | ---: |
| 0261 | Minimal EOL bailout/state-corruption mitigation | 19,668 |
| 0262 | Emit the file-count-limit warning only once | 964 |
| 0263 | Introduce `max_multipart_body_parts` | 2,491 |

The full filenames and byte hashes are in [patches.sha256](patches.sha256).
Only these three patches are added to the existing Debian series. This project
does not import the complete Sury packaging or its Debian 11 binary packages.

## 0261: allocation failure and request cleanup

The patch describes itself as a minimal mitigation for an EOL version and cites:

- [GHSA-w8hw-w9fx-j79w / CVE-2026-109618](https://github.com/php/php-src/security/advisories/GHSA-w8hw-w9fx-j79w)
- [GHSA-6wmf-4rv5-p3rp / CVE-2026-109619](https://github.com/php/php-src/security/advisories/GHSA-6wmf-4rv5-p3rp)

It adds `zend_mm_safe_error_ex()` and directs selected allocation/overflow failure
paths to `_exit(1)`. It also clears request/executor/list pointers and state during
teardown, introduces a small-array initializer for selected GPC arrays, and
changes multipart header handling and length types.

### Behavior operators must account for

- Selected OOM/overflow failures terminate the process immediately. PHP shutdown
  functions, destructors, and normal response completion may not run.
- With mod_php, that process is an Apache worker. The parent replaced the worker
  in the isolated acceptance test; the interrupted request can still fail.
- The session upload-progress callback contains an unconditional early-return
  condition. Setting `session.upload_progress.enabled=On` does not restore that
  feature in this runtime.
- Ordinary uploads are still intended to work, and selected multipart/raw-upload
  paths were exercised. This is not a guarantee for every input or application.

## 0262: repeated warnings

After `max_file_uploads` is exceeded, the warning is emitted once rather than
repeated for each additional file. This patch adds no INI setting.

## 0263: multipart part count

This patch cites
[GHSA-54hq-v5wp-fqgv / CVE-2023-0662](https://github.com/php/php-src/security/advisories/GHSA-54hq-v5wp-fqgv).

`max_multipart_body_parts` defaults to `-1`. A negative value derives the effective
limit from `max_input_vars + max_file_uploads`. Its changeability is
`PHP_INI_SYSTEM | PHP_INI_PERDIR`. Exceeding the limit produces a warning and ends
multipart processing.

This setting counts parts. It is not a byte-size upload limit and does not change
`upload_max_filesize` or `post_max_size`.

## Runtime files touched by the added patches

`Zend/zend_API.c`, `Zend/zend_API.h`, `Zend/zend_alloc.c`, `Zend/zend_alloc.h`,
`Zend/zend_execute_API.c`, `Zend/zend_llist.c`, `Zend/zend_operators.c`,
`Zend/zend_strtod.c`, `ext/session/session.c`, `main/SAPI.c`, `main/main.c`,
`main/php_variables.c`, and `main/rfc1867.c`.

There are 13 distinct existing runtime files. These three patches add no separate
runtime file or regression-test suite. They were applied without fuzz; line
offsets were permitted. Package versions must be checked with `dpkg-query`:
the upstream version number alone remains 5.6.40.
