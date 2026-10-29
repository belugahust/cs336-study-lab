$ErrorActionPreference = 'Stop'
$studyRoot = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $studyRoot

function Assert-CommandSuccess([string]$step) {
    if ($LASTEXITCODE -ne 0) { throw "$step failed. Read the error above, then rerun this script." }
}

Write-Host 'Step 1/4: Check Python (3.11+ required).'
& python -c "import sys; print(sys.version); assert sys.version_info >= (3, 11), 'Python 3.11+ required'"
Assert-CommandSuccess 'Python check'

$toolsPython = Join-Path $studyRoot '.tools/Scripts/python.exe'
if (-not (Test-Path -LiteralPath $toolsPython)) {
    & python -m venv (Join-Path $studyRoot '.tools')
    Assert-CommandSuccess 'Create project tool environment'
}
Write-Host 'Step 2/4: Install uv in the project tool environment (not globally).'
& $toolsPython -m pip install --timeout 30 --retries 1 uv
Assert-CommandSuccess 'Install uv'

Set-Location -LiteralPath (Join-Path $studyRoot 'assignments/01-basics')
Write-Host 'Step 3/4: Install the locked A1 environment. Downloads may take time.'
& $toolsPython -m uv sync --frozen --python 3.11
Assert-CommandSuccess 'Install A1 dependencies'

Write-Host 'Step 4/4: Verify imports and collect tests (not solve them).'
& $toolsPython -m uv run --frozen python -c "import sys, torch, pytest, regex; print('Python:', sys.executable); print('PyTorch:', torch.__version__); print('CUDA:', torch.cuda.is_available())"
Assert-CommandSuccess 'Import check'
& $toolsPython -m uv run --frozen pytest tests/test_train_bpe.py --collect-only -q
Assert-CommandSuccess 'Collect BPE tests'

Set-Location -LiteralPath $studyRoot
Write-Host 'Ready. Open assignments/01-basics/BEGINNER_START_HERE.md for your first exercise.'
