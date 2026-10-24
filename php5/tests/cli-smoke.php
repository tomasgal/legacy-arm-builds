<?php
// SPDX-License-Identifier: MIT
// Run with the intended PHP binary and configuration; APCu CLI must be enabled.
$required = array('json', 'apcu', 'curl', 'gd', 'gmp', 'intl', 'mcrypt',
                  'mysql', 'mysqli', 'PDO', 'pdo_mysql');
if (count(array_diff($required, get_loaded_extensions()))) {
    fwrite(STDERR, "EXTENSIONS_FAIL\n");
    exit(1);
}
if (!array_key_exists('max_multipart_body_parts', ini_get_all()) ||
    !function_exists('opcache_get_status') ||
    json_decode(json_encode(array('ok' => 42)), true) !== array('ok' => 42) ||
    !apcu_store('legacy_arm_smoke', 42) || apcu_fetch('legacy_arm_smoke') !== 42 ||
    imagecreatetruecolor(2, 2) === false ||
    gmp_strval(gmp_add('40', '2')) !== '42' ||
    Normalizer::normalize('test') !== 'test') {
    fwrite(STDERR, "RUNTIME_FAIL\n");
    exit(1);
}
apcu_delete('legacy_arm_smoke');
echo 'PHP=', PHP_VERSION, "\nCLI_SMOKE_OK\n";
