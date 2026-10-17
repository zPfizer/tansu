param([switch]$Belge)

# Test gate. Run it from any folder. The PR body does not take the "kapi:" lines; CI proves the tests.
# A command that cannot start stops the script (python, git). Native stderr is not redirected.
$ErrorActionPreference = 'Stop'
Set-Location (Split-Path -Parent $PSScriptRoot)
$py = if ($env:TANSU_PY) { $env:TANSU_PY } else { 'C:\Users\levent\Desktop\TANSU\.venv\Scripts\python.exe' }
if (-not (Test-Path -LiteralPath $py)) {
    "kapi: python yok: $py"
    exit 1
}

# Always count the open pool notes. A missing pool folder stops the gate.
# The count must be a whole number. Empty or bad output stops the gate.
# A set variable wins: the count only sets the variable when it is unset.
$acikSayi = & $py -X utf8 tests/atif_araclari.py acik-sayi
if ($LASTEXITCODE -ne 0) {
    'kapi: acik havuz notu = HATA'
    exit 1
}
if ("$acikSayi" -notmatch '^\d+$') {
    "kapi: acik havuz notu = HATA (gecersiz sayi: $acikSayi)"
    exit 1
}
"kapi: acik havuz notu = $acikSayi"
if (-not $env:TANSU_BEKLENEN_ACIK -and [int]$acikSayi -gt 0) { $env:TANSU_BEKLENEN_ACIK = "$acikSayi" }

if ($Belge) {
    & $py -m pytest -q tests/test_atif.py tests/test_havuz.py tests/test_sahipler.py tests/test_standartlar.py tests/test_dod_kontrol.py
    $pytestKod = $LASTEXITCODE
    $pytestAd = 'pytest (belge)'
} else {
    & $py -m pytest -q
    $pytestKod = $LASTEXITCODE
    $pytestAd = 'pytest'
}
& $py -m ruff check .
$checkKod = $LASTEXITCODE
& $py -m ruff format --check .
$formatKod = $LASTEXITCODE
git diff --check origin/master
$diffKod = $LASTEXITCODE

$sha = (git rev-parse HEAD)
if ($LASTEXITCODE -ne 0 -or "$sha" -notmatch '^[0-9a-f]{40}$') {
    "kapi: git rev-parse HEAD = HATA ($sha)"
    exit 1
}
$kirli = git status --porcelain
if ($LASTEXITCODE -ne 0) {
    'kapi: git status = HATA'
    exit 1
}
$durum = if ($kirli) { 'kirli' } else { 'temiz' }
$acik = if ($env:TANSU_BEKLENEN_ACIK) { $env:TANSU_BEKLENEN_ACIK } else { 'yok' }
$parti = if ($env:TANSU_PARTI) { $env:TANSU_PARTI } else { 'yok' }

"kapi: $pytestAd -> $pytestKod"
"kapi: ruff check -> $checkKod"
"kapi: ruff format -> $formatKod"
"kapi: git diff --check -> $diffKod"
"kapi: TANSU_BEKLENEN_ACIK=$acik"
"kapi: TANSU_PARTI=$parti"
"kapi: HEAD $sha $durum"

if ($pytestKod -ne 0 -or $checkKod -ne 0 -or $formatKod -ne 0 -or $diffKod -ne 0) { exit 1 }
exit 0
