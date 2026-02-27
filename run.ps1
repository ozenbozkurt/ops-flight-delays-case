[CmdletBinding()]
param(
  [switch]$RecreateVenv,
  [switch]$SkipInstall,
  [switch]$CleanOutputs,
  [switch]$SkipSampleGen
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$RepoRoot = $PSScriptRoot
Push-Location $RepoRoot
try {
  $VenvDir = Join-Path $RepoRoot ".venv"
  $PyVenv  = Join-Path $VenvDir "Scripts\python.exe"

  if ($RecreateVenv -and (Test-Path $VenvDir)) {
    Write-Host "[VENVDIR] Removing existing venv: $VenvDir"
    Remove-Item -Recurse -Force $VenvDir
  }

  if (-not (Test-Path $PyVenv)) {
    Write-Host "[VENV] Creating venv..."
    $pyCmd = Get-Command py -ErrorAction SilentlyContinue
    $pythonCmd = Get-Command python -ErrorAction SilentlyContinue

    if ($pyCmd) {
      & $pyCmd.Source -3 -m venv $VenvDir
    } elseif ($pythonCmd) {
      & $pythonCmd.Source -m venv $VenvDir
    } else {
      throw "Python not found. Install Python 3.x and ensure 'python' or 'py' is on PATH."
    }
  }

  if (-not $SkipInstall) {
    Write-Host "[PIP] Installing requirements..."
    & $PyVenv -m pip install --upgrade pip | Out-Host
    if (-not (Test-Path (Join-Path $RepoRoot "requirements.txt"))) {
      throw "requirements.txt missing in repo root."
    }
    & $PyVenv -m pip install -r "requirements.txt" | Out-Host
  }

  if ($CleanOutputs) {
    $outDir = Join-Path $RepoRoot "outputs"
    if (Test-Path $outDir) {
      Write-Host "[CLEAN] Cleaning outputs/ ..."
      Get-ChildItem -Path $outDir -File -ErrorAction SilentlyContinue | Remove-Item -Force -ErrorAction SilentlyContinue
    }
  }

  $Sample = Join-Path $RepoRoot "data\sample_multi_month.csv"
  if (-not $SkipSampleGen) {
    $Big1 = Join-Path $RepoRoot "ops-bigdata\flight_data_2024.csv"
    $Big2 = Join-Path $HOME "Desktop\ops-bigdata\flight_data_2024.csv"
    $Big3 = Join-Path $HOME "Masaustuu\ops-bigdata\flight_data_2024.csv"
    $HasBig = (Test-Path $Big1) -or (Test-Path $Big2) -or (Test-Path $Big3)

    if ($HasBig -and (Test-Path (Join-Path $RepoRoot "analysis.py"))) {
      Write-Host "[DATA] Generating data\sample_multi_month.csv (from big CSV)..."
      & $PyVenv "analysis.py" | Out-Host
    } elseif (-not (Test-Path $Sample)) {
      throw "Missing data\sample_multi_month.csv AND big dataset not found. Put flight_data_2024.csv in ops-bigdata\ or Desktop\ops-bigdata\ then re-run."
    } else {
      Write-Host "[DATA] Using existing data\sample_multi_month.csv"
    }
  }

  $steps = @("analysis_eda.py", "analysis_ops.py", "main.py")
  foreach ($s in $steps) {
    $p = Join-Path $RepoRoot $s
    if (Test-Path $p) {
      Write-Host "[RUN] Running $s ..."
      & $PyVenv $p | Out-Host
    } else {
      Write-Host "[SKIP] Skip (missing): $s"
    }
  }

  Write-Host "[DONE] Done. Check outputs/"
}
finally {
  Pop-Location
}