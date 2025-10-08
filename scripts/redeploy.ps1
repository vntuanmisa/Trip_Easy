Param(
  [string]$CommitMessage = "chore: auto commit and redeploy",
  [string]$BackendDir = "backend",
  [string]$FrontendDir = "frontend",
  [string]$BackendAlias = "",
  [string]$FrontendAlias = ""
)

function Write-Info($msg) {
  Write-Host "[TripEasy] $msg" -ForegroundColor Cyan
}

function Require-Command($name) {
  $exists = Get-Command $name -ErrorAction SilentlyContinue
  return $null -ne $exists
}

$ErrorActionPreference = "Stop"

Write-Info "Starting redeploy pipeline..."

if (-not $env:VERCEL_TOKEN) {
  Write-Error "VERCEL_TOKEN environment variable is required. Set it before running this script."
  exit 1
}

$useVercelCmd = ""
if (Require-Command "vercel") {
  $useVercelCmd = "vercel"
} elseif (Require-Command "npx") {
  $useVercelCmd = "npx vercel@latest"
} else {
  Write-Error "Neither 'vercel' nor 'npx' is available. Please install Node.js (which provides npx) or the Vercel CLI."
  exit 1
}

# 1) Commit & push
Write-Info "Committing and pushing changes..."
git add . | Out-Null
try {
  git commit -m $CommitMessage | Out-Null
} catch {
  Write-Info "No changes to commit. Proceeding..."
}
git push | Out-Null

function Deploy-With-Vercel($projectDir, $alias) {
  Push-Location $projectDir
  try {
    Write-Info "Deploying project at '$projectDir'..."
    & $useVercelCmd env pull .env.local --yes --token $env:VERCEL_TOKEN | Out-Null

    if (Test-Path package.json) {
      if (Test-Path package-lock.json) {
        Write-Info "Installing dependencies with npm ci..."
        npm ci | Out-Null
      } else {
        Write-Info "Installing dependencies with npm install..."
        npm install | Out-Null
      }
      if ((Get-Content package.json | Select-String -SimpleMatch '"build"')) {
        Write-Info "Building project..."
        npm run build | Out-Null
      }
    }

    $deployOutput = & $useVercelCmd deploy --prod --yes --token $env:VERCEL_TOKEN 2>&1
    $urls = ($deployOutput | Select-String -Pattern 'https://[a-zA-Z0-9-]+\.vercel\.app' -AllMatches).Matches.Value
    $deploymentUrl = $urls | Select-Object -Last 1
    if (-not $deploymentUrl) {
      Write-Warning "Could not detect deployment URL from Vercel output."
    } else {
      Write-Info "Deployed: $deploymentUrl"
    }

    if ($alias -and $deploymentUrl) {
      Write-Info "Mapping alias '$alias' to deployment..."
      & $useVercelCmd alias set $deploymentUrl $alias --token $env:VERCEL_TOKEN | Out-Null
      Write-Info "Alias mapped: https://$alias"
    }

    return $deploymentUrl
  } finally {
    Pop-Location
  }
}

$backendUrl = Deploy-With-Vercel -projectDir $BackendDir -alias $BackendAlias
$frontendUrl = Deploy-With-Vercel -projectDir $FrontendDir -alias $FrontendAlias

Write-Host ""  # newline
Write-Info "Redeploy finished. Summary:"
if ($backendUrl) { Write-Host "  Backend: $backendUrl" }
if ($BackendAlias) { Write-Host "  Backend Alias: https://$BackendAlias" }
if ($frontendUrl) { Write-Host "  Frontend: $frontendUrl" }
if ($FrontendAlias) { Write-Host "  Frontend Alias: https://$FrontendAlias" }

exit 0


