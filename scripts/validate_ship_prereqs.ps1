# Pre-ship validation (no secrets required)
$ErrorActionPreference = "Continue"
$fail = 0

function Test-Url {
    param([string]$Url, [string]$Label, [string]$Match = "")
    try {
        $r = Invoke-WebRequest -Uri $Url -UseBasicParsing -TimeoutSec 30
        if ($r.StatusCode -ge 200 -and $r.StatusCode -lt 400) {
            if ($Match -and $r.Content -notmatch $Match) {
                Write-Host "WARN $Label — HTTP $($r.StatusCode) but body mismatch"
                return $false
            }
            Write-Host "OK   $Label"
            return $true
        }
    } catch {
        Write-Host "FAIL $Label — $_"
        return $false
    }
    Write-Host "FAIL $Label — status $($r.StatusCode)"
    return $false
}

Write-Host "SeedJournal ship prereqs`n"

if (-not (Test-Url "https://minaelzek.github.io/SeedJournalV1/privacy/" "Privacy (GitHub Pages)" "Privacy")) { $fail++ }

$staging = "https://seedjournal-api-staging.fly.dev/health"
try {
    $r = Invoke-WebRequest -Uri $staging -UseBasicParsing -TimeoutSec 20
    if ($r.Content -match '"status"\s*:\s*"ok"') {
        Write-Host "OK   Staging API health"
    } else {
        Write-Host "WARN Staging reachable but unexpected body"
        $fail++
    }
} catch {
    Write-Host "SKIP Staging API (not deployed yet; complete Gate 2 in SHIP_CHECKLIST.md)"
}

$root = Split-Path $PSScriptRoot -Parent
$required = @(
    "docs\SHIP_CHECKLIST.md",
    "backend\fly.staging.toml",
    "ios\Config\Staging.xcconfig"
)
foreach ($rel in $required) {
    $p = Join-Path $root $rel
    if (Test-Path $p) { Write-Host "OK   file $rel" } else { Write-Host "FAIL missing $rel"; $fail++ }
}

Write-Host ""
if ($fail -eq 0) {
    Write-Host "Prereqs OK (staging may still be pending deploy)."
    exit 0
}
Write-Host "$fail check(s) failed."
exit 1