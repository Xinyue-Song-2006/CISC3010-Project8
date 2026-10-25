$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $PSScriptRoot
$pythonCandidates = @(
  'C:\PROGRA~2\MICROS~3\Shared\Python39_64\python.exe',
  'C:\Program Files\Microsoft Visual Studio\Shared\Python39_64\python.exe',
  (Join-Path $Root '..\.venv\Scripts\python.exe')
)
$pythonCommand = Get-Command python -ErrorAction SilentlyContinue
if ($null -ne $pythonCommand) { $pythonCandidates += 'python' }
$Python = $null
foreach ($candidate in ($pythonCandidates | Where-Object { $_ } | Select-Object -Unique)) {
  $isAbsolutePath = [System.IO.Path]::IsPathRooted($candidate)
  if ($isAbsolutePath -and -not (Test-Path -LiteralPath $candidate)) { continue }
  if (-not $isAbsolutePath -and $null -eq (Get-Command $candidate -ErrorAction SilentlyContinue)) { continue }
  $savedErrorActionPreference = $ErrorActionPreference
  $ErrorActionPreference = 'Continue'
  & $candidate -c "import pyspark" 2>$null | Out-Null
  $candidateExitCode = $LASTEXITCODE
  $ErrorActionPreference = $savedErrorActionPreference
  if ($candidateExitCode -eq 0) { $Python = $candidate; break }
}
if ($null -eq $Python) {
  throw 'No Python interpreter with PySpark was found. Install pyspark or update the Python path in this script.'
}
$jdk11 = Join-Path $Root '..\tools\jdk11\jdk-11.0.32.1+1'
$jdk17 = Join-Path $Root '..\tools\jdk17\jdk-17.0.20.1+1'
if (Test-Path $jdk11) { $env:JAVA_HOME = (Resolve-Path $jdk11).Path } elseif (Test-Path $jdk17) { $env:JAVA_HOME = (Resolve-Path $jdk17).Path }
$env:PYSPARK_PYTHON = $Python
$env:PYSPARK_DRIVER_PYTHON = $Python
& $Python (Join-Path $Root 'src\run_experiment.py') --repeats 2 --iterations 6 --partitions 4
& $Python (Join-Path $Root 'src\analyze_results.py') --results (Join-Path $Root 'results\raw_runs.csv') --out-dir (Join-Path $Root 'results')
