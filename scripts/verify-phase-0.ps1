# Phase 0 Verification Script
# Run this script to verify Phase 0 setup is complete

Write-Host "`n=== Splay Phase 0 Verification ===" -ForegroundColor Cyan
Write-Host "This script will check if all Phase 0 components are properly set up.`n"

$allPassed = $true

# Check 1: Docker Desktop running
Write-Host "Checking Docker Desktop..." -NoNewline
try {
    $dockerInfo = docker ps 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host " ✓ Running" -ForegroundColor Green
    } else {
        Write-Host " ✗ Not running" -ForegroundColor Red
        Write-Host "  Please start Docker Desktop and try again." -ForegroundColor Yellow
        $allPassed = $false
    }
} catch {
    Write-Host " ✗ Not installed or not running" -ForegroundColor Red
    $allPassed = $false
}

# Check 2: PostgreSQL container
Write-Host "Checking PostgreSQL container..." -NoNewline
try {
    $pgContainer = docker ps --filter "name=splay_postgres" --format "{{.Status}}"
    if ($pgContainer -match "healthy|Up") {
        Write-Host " ✓ Running" -ForegroundColor Green
    } else {
        Write-Host " ✗ Not running" -ForegroundColor Red
        Write-Host "  Run: cd infra\docker && docker-compose up -d" -ForegroundColor Yellow
        $allPassed = $false
    }
} catch {
    Write-Host " ✗ Error" -ForegroundColor Red
    $allPassed = $false
}

# Check 3: Redis container
Write-Host "Checking Redis container..." -NoNewline
try {
    $redisContainer = docker ps --filter "name=splay_redis" --format "{{.Status}}"
    if ($redisContainer -match "healthy|Up") {
        Write-Host " ✓ Running" -ForegroundColor Green
    } else {
        Write-Host " ✗ Not running" -ForegroundColor Red
        Write-Host "  Run: cd infra\docker && docker-compose up -d" -ForegroundColor Yellow
        $allPassed = $false
    }
} catch {
    Write-Host " ✗ Error" -ForegroundColor Red
    $allPassed = $false
}

# Check 4: Python dependencies
Write-Host "Checking Python dependencies..." -NoNewline
$requirementsPath = ".\apps\api\requirements.txt"
if (Test-Path $requirementsPath) {
    Write-Host " ✓ requirements.txt exists" -ForegroundColor Green
} else {
    Write-Host " ✗ requirements.txt not found" -ForegroundColor Red
    $allPassed = $false
}

# Check 5: Alembic migrations directory
Write-Host "Checking migrations..." -NoNewline
$migrationsPath = ".\apps\api\alembic\versions\001_initial.py"
if (Test-Path $migrationsPath) {
    Write-Host " ✓ Initial migration exists" -ForegroundColor Green
} else {
    Write-Host " ✗ Initial migration not found" -ForegroundColor Red
    $allPassed = $false
}

# Check 6: FastAPI main file
Write-Host "Checking FastAPI app..." -NoNewline
$mainPath = ".\apps\api\app\main.py"
if (Test-Path $mainPath) {
    Write-Host " ✓ main.py exists" -ForegroundColor Green
} else {
    Write-Host " ✗ main.py not found" -ForegroundColor Red
    $allPassed = $false
}

# Check 7: Models directory
Write-Host "Checking database models..." -NoNewline
$modelsPath = ".\apps\api\app\models"
if (Test-Path $modelsPath) {
    $modelFiles = @("user.py", "scan.py", "product.py")
    $allModelsExist = $true
    foreach ($file in $modelFiles) {
        if (-not (Test-Path "$modelsPath\$file")) {
            $allModelsExist = $false
            break
        }
    }
    if ($allModelsExist) {
        Write-Host " ✓ All models exist" -ForegroundColor Green
    } else {
        Write-Host " ✗ Some models missing" -ForegroundColor Red
        $allPassed = $false
    }
} else {
    Write-Host " ✗ Models directory not found" -ForegroundColor Red
    $allPassed = $false
}

# Check 8: Environment file
Write-Host "Checking environment configuration..." -NoNewline
$envPath = ".\infra\docker\.env"
if (Test-Path $envPath) {
    Write-Host " ✓ .env file exists" -ForegroundColor Green
} else {
    Write-Host " ⚠ .env file not found (using .env.example as template)" -ForegroundColor Yellow
}

# Summary
Write-Host "`n=== Verification Summary ===" -ForegroundColor Cyan
if ($allPassed) {
    Write-Host "✓ All Phase 0 checks passed!" -ForegroundColor Green
    Write-Host "`nNext steps:"
    Write-Host "1. Activate Python venv: cd apps\api && venv\Scripts\activate"
    Write-Host "2. Install dependencies: pip install -r requirements.txt"
    Write-Host "3. Run migrations: alembic upgrade head"
    Write-Host "4. Start API: uvicorn app.main:app --reload"
    Write-Host "5. Verify: http://localhost:8000/health"
    Write-Host "`nSee SETUP_INSTRUCTIONS.md for detailed steps."
} else {
    Write-Host "✗ Some checks failed. Please review the errors above." -ForegroundColor Red
    Write-Host "`nRefer to SETUP_INSTRUCTIONS.md for troubleshooting help."
}

Write-Host ""
