# Legacy ARM Builds

Selected source rebuilds for legacy ARM systems, with pinned inputs, retained
upstream attribution, explicit compatibility limits, and release checksums.

## PHP 5.6.40 for Debian Jessie / armhf

The first build combines Debian's `php5 5.6.40+dfsg-0+deb8u12` packaging with
three selected patches from the DEB.SURY.ORG PHP 5.6 packaging. The deployed
package revision is `5.6.40+dfsg-0+deb8u12+local20261023.1`.

| Item | Status |
| --- | --- |
| Pinned source inputs and three vendor patches | Included |
| Source preparation recipe | Included; see its validation limits |
| Native armhf build and selected runtime smoke tests | Reported PASS on 24 October 2026 |
| Twelve original native `.deb` files | Included in the [versioned release](https://github.com/tomasgal/legacy-arm-builds/releases/tag/php5-jessie-armhf-local20261023.1) |
| Exact corresponding source package for those binaries | Exported and verified against the original pre-build tree |
| Binary GitHub Release | [php5-jessie-armhf-local20261023.1](https://github.com/tomasgal/legacy-arm-builds/releases/tag/php5-jessie-armhf-local20261023.1) |

**This is a targeted mitigation for end-of-life software.** It does not restore
general security support for PHP 5.6 or Debian Jessie, and it does not contain
the complete current Sury patch set. No compatibility with arbitrary ARM systems
or current distributions is claimed.

The tested platform was Debian 8 Jessie, ARMv7/armhf, an Orange Pi Plus 2, and
Apache 2.4.10 with prefork/mod_php. CLI and an isolated Apache instance were
tested. FPM was packaged and installed, but its request processing was not
independently exercised.

The bailout mitigation changes failure handling: selected allocation failures
terminate the process immediately, without normal PHP shutdown callbacks or
destructors. In mod_php, the Apache worker may terminate. The patch also disables
PHP session upload progress in code. Read the [patch manifest](php5/PATCHES.md)
before evaluating a deployment.

The release retains the original binary bytes and original local changelog. It includes the full Debian source package, checksums, and third-party notices. The source preparation helper remains a distinct `+rebuild1` recipe.

## Contents

- [Source provenance and hashes](php5/PROVENANCE.md)
- [Patch manifest and behavior changes](php5/PATCHES.md)
- [Source preparation and native build procedure](php5/BUILD.md)
- [Recorded validation and limitations](php5/VALIDATION.md)
- [Release publication requirements](php5/RELEASE.md)
- [Machine-readable artifact plan](php5/release-plan.json)
- [Selected binary verifier](php5/verify-debs.py)

Binary packages belong in GitHub Releases, alongside complete corresponding
source and checksums. They are not stored in the Git source history. There is no
automatic installer, production configuration, or APT repository in this project.

## Attribution and licenses

PHP is developed by the PHP Group and its contributors. Debian packaging and the
selected backports retain their respective upstream authorship and licenses.
This product includes PHP software, freely available from
<https://www.php.net/software/>.

See [LICENSE.md](LICENSE.md) for the distinction between the original project
helpers and third-party PHP/packaging material.
