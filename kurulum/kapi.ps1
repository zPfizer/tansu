param([switch]$Belge)

# Test gate. Run it from any folder. Paste the "kapi:" lines into the PR body.
Set-Location (Split-Path -Parent $PSScriptRoot)
$py = 'C:\Users\levent\Desktop\TANSU\.venv\Scripts\python.exe'

# Count the open pool notes unless the variable is set. A set variable wins.
if (-not $env:TANSU_BEKLENEN_ACIK) {
    if (Test-Path (Join-Path $HOME 'Desktop\YONETIM\beyin\kisisel\300-Projects\Tansu X Veri Havuzu')) {
        $acikSayi = & $py -X utf8 tests/atif_araclari.py acik-sayi
        if ($LASTEXITCODE -ne 0) {
            'kapi: acik havuz notu = HATA'
            exit 1
        }
        "kapi: acik havuz notu = $acikSayi"
        if ([int]$acikSayi -gt 0) { $env:TANSU_BEKLENEN_ACIK = "$acikSayi" }
    } else {
        'kapi: acik havuz notu = yok'
    }
}

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
git diff --check kaynak/master
$diffKod = $LASTEXITCODE

$sha = (git rev-parse HEAD)
$kirli = git status --porcelain
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
