# Run an A1 command using the project-local uv installation.
# From the repository root: powershell -ExecutionPolicy Bypass -File scripts/a1.ps1 pytest ...
$ErrorActionPreference = 'Stop'
$studyRoot = Split-Path -Parent $PSScriptRoot
$toolsPython = Join-Path $studyRoot '.tools/Scripts/python.exe'
if (-not (Test-Path -LiteralPath $toolsPython)) {
    throw 'Run scripts/setup-a1.ps1 first to install the project-local uv tool.'
}
Set-Location -LiteralPath (Join-Path $studyRoot 'assignments/01-basics')
& $toolsPython -m uv run --frozen @args
exit $LASTEXITCODE
