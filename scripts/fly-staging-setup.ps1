# SeedJournal — Fly staging setup (Windows PowerShell)
# Prereqs: flyctl installed, Neon DATABASE_URL ready
# Usage: edit variables below, then: .\scripts\fly-staging-setup.ps1

$ErrorActionPreference = "Stop"
$AppName = "seedjournal-api-staging"

Write-Host "Login to Fly if needed: fly auth login"
Write-Host "App name: $AppName"
Write-Host ""
Write-Host "Set secrets manually (paste real values):"
Write-Host @"
  cd backend
  fly apps create $AppName
  fly secrets set -a $AppName `
    DATABASE_URL="postgresql+asyncpg://..." `
    JWT_SECRET="$( -join ((48..57)+(65..90)+(97..122) | Get-Random -Count 64 | ForEach-Object {[char]$_}) )" `
    APPLE_CLIENT_ID="com.seedjournal.app" `
    APP_ENV="production" `
    LLM_PROVIDER="openai" `
    OPENAI_API_KEY="sk-..." `
    CORS_ORIGINS="https://minaelzek.github.io"
  fly deploy -a $AppName
"@

Write-Host ""
Write-Host "Then: bash scripts/smoke_staging.sh https://$AppName.fly.dev"