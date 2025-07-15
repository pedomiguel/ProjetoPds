# 1. Start PostgreSQL with Docker Compose
Write-Host "=== 1. Starting PostgreSQL with Docker Compose ==="
docker-compose up -d

# 2. Set up Python virtual environment with uv
Write-Host "=== 2. Setting up Python virtual environment with uv ==="
if (-Not (Test-Path ".venv")) {
    uv venv
}

# 3. Activate venv
Write-Host "=== 3. Activating virtual environment ==="
. .\.venv\Scripts\Activate.ps1

# 4. Install dependencies with uv
Write-Host "=== 4. Installing dependencies with uv ==="
uv sync

# 5. Install extractor app dependencies
Write-Host "=== 5. Installing extractor app dependencies ==="
uv pip install -r app\extractor_app\requirements.txt
Write-Host "Extractor dependencies installed successfully."

# 6. Check for .env file
Write-Host "=== 6. Checking for .env file ==="
if (-Not (Test-Path ".env")) {
    Write-Host "No .env file found! Please create one with your DB and secret config."
    Write-Host "Example:"
    Write-Host "DATABASE_URL=postgresql://postgres:1234@localhost:5432/musicdb"
    Write-Host "SECRET_KEY=your_secret_key"
    Write-Host "ACCESS_TOKEN_EXPIRE_MINUTES=60"
    Write-Host "ALGORITHM=HS256"
    exit 1
}

# 7. Remind about model checkpoints and configs
Write-Host "=== 7. REMINDER: Place your model checkpoi nts and config files ==="
Write-Host "  - .ckpt files in app\extractor_app\configs\ckpt\"
Write-Host "  - .yaml config files in app\extractor_app\configs\gabox_melroformer\"
Read-Host "Press Enter to continue..."

# 8. Run Alembic migrations (if used)
if (Test-Path "alembic") {
    Write-Host "=== 8. Running database migrations (Alembic) ==="
    alembic upgrade head
} else {
    Write-Host "No Alembic migrations found. Skipping."
}

# 8. Create uploads directory if it doesn't exist
Write-Host "=== 8. Creating 'uploads' directory if needed ==="
mkdir uploads -Force | Out-Null

# 9. Start FastAPI app with Uvicorn
Write-Host "=== 9. Starting FastAPI app with Uvicorn ==="
python -m uvicorn main:app --reload 