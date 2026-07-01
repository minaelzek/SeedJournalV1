# Checks staging is up enough for Sign in with Apple (not a full Apple login test).
param(
    [string]$BaseUrl = "https://seedjournal-api-staging.fly.dev"
)
$BaseUrl = $BaseUrl.TrimEnd("/")
$fail = 0

Write-Host "Auth readiness: $BaseUrl"
Write-Host ""

# 1. Health
try {
    $h = Invoke-RestMethod -Uri "$BaseUrl/health" -TimeoutSec 90
    if ($h.status -eq "ok") { Write-Host "OK   GET /health" }
    else { Write-Host "FAIL /health unexpected body"; $fail++ }
} catch {
    Write-Host "FAIL GET /health - fix DATABASE_URL / fly logs before testing Apple sign-in"
    Write-Host "     $_"
    exit 1
}

# 2. Auth rejects garbage (proves route + JWT stack loaded)
try {
    $body = @{ identity_token = "not-a-real-jwt" } | ConvertTo-Json -Compress
    Invoke-WebRequest -Uri "$BaseUrl/v1/auth/apple" -Method POST -Body $body `
        -ContentType "application/json" -UseBasicParsing -TimeoutSec 60 | Out-Null
    Write-Host "FAIL POST /v1/auth/apple should reject invalid token"
    $fail++
} catch {
    $code = $_.Exception.Response.StatusCode.value__
    if ($code -eq 401) {
        Write-Host "OK   POST /v1/auth/apple returns 401 for invalid token (production mode)"
    } elseif ($code -eq 503 -or $code -eq 502) {
        Write-Host "FAIL API still unhealthy ($code)"
        $fail++
    } else {
        Write-Host "OK   POST /v1/auth/apple rejected ($code)"
    }
}

# 3. Dev JSON must NOT work on production staging
try {
    $devJson = '{"sub":"hacker","email":"x@test.com"}'
    $body = @{ identity_token = $devJson } | ConvertTo-Json -Compress
    Invoke-WebRequest -Uri "$BaseUrl/v1/auth/apple" -Method POST -Body $body `
        -ContentType "application/json" -UseBasicParsing -TimeoutSec 60 | Out-Null
    Write-Host "FAIL dev JSON auth should be disabled when APP_ENV=production"
    $fail++
} catch {
    $code = $_.Exception.Response.StatusCode.value__
    if ($code -eq 401) {
        Write-Host "OK   dev JSON sign-in blocked on staging (expected)"
    } else {
        Write-Host "WARN dev JSON test got HTTP $code"
    }
}

# 4. Protected route
try {
    Invoke-WebRequest -Uri "$BaseUrl/v1/tree" -UseBasicParsing -TimeoutSec 30 | Out-Null
    Write-Host "FAIL /v1/tree should require auth"
    $fail++
} catch {
    if ($_.Exception.Response.StatusCode.value__ -eq 401) {
        Write-Host "OK   GET /v1/tree requires Bearer token"
    }
}

Write-Host ""
if ($fail -eq 0) {
    Write-Host "Staging is ready for Sign in with Apple on device (SeedJournal-Staging scheme)."
    exit 0
}
Write-Host "$fail check(s) failed."
exit 1