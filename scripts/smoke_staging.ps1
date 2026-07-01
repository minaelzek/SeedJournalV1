param(
    [Parameter(Mandatory = $true)]
    [string]$BaseUrl
)

$BaseUrl = $BaseUrl.TrimEnd("/")

function Test-Endpoint {
    param([string]$Path, [string]$Label)
    $uri = "$BaseUrl$Path"
    try {
        $r = Invoke-WebRequest -Uri $uri -UseBasicParsing -TimeoutSec 60
        if ($r.StatusCode -ge 200 -and $r.StatusCode -lt 300) {
            Write-Host "OK $Label ($uri)"
            return $r.Content
        }
    } catch {
        Write-Error "FAIL $Label ($uri): $_"
        exit 1
    }
}

Write-Host "Smoke test: $BaseUrl"
$c1 = Test-Endpoint "/health" "health"
if ($c1 -notmatch '"status"\s*:\s*"ok"') { Write-Error "Unexpected /health body"; exit 1 }

$c2 = Test-Endpoint "/v1/health" "v1 health"
if ($c2 -notmatch '"status"\s*:\s*"ok"') { Write-Error "Unexpected /v1/health body"; exit 1 }

try {
    $null = Invoke-WebRequest -Uri "$BaseUrl/openapi.json" -UseBasicParsing -TimeoutSec 60
    Write-Host "OK openapi.json"
} catch {
    Write-Warning "openapi.json not reachable (non-fatal): $_"
}

Write-Host ""
Write-Host "Smoke passed for $BaseUrl"
Write-Host "Next: Sign in with Apple on device (SeedJournal-Staging scheme)."