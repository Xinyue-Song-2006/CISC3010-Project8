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
$PySparkRoot = (& $Python -c "import pyspark, pathlib; print(pathlib.Path(pyspark.__file__).resolve().parent)").Trim()
$SparkSubmit = Join-Path $PySparkRoot 'bin\spark-submit.cmd'
$jdk11 = Join-Path $Root '..\tools\jdk11\jdk-11.0.32.1+1'
$jdk17 = Join-Path $Root '..\tools\jdk17\jdk-17.0.20.1+1'
if (Test-Path $jdk11) { $env:JAVA_HOME = (Resolve-Path $jdk11).Path } elseif (Test-Path $jdk17) { $env:JAVA_HOME = (Resolve-Path $jdk17).Path }
$env:PYSPARK_PYTHON = $Python
$env:PYSPARK_DRIVER_PYTHON = $Python
New-Item -ItemType Directory -Force (Join-Path $Root 'results') | Out-Null
& $Python (Join-Path $Root 'data\generate_data.py') --nodes 1000 --edges 5000 --out (Join-Path $Root 'data\sample_edges.txt')
foreach ($Mode in @('uncached','cached')) {
  $Output = Join-Path $Root "results\demo_$Mode.json"
  $CacheArg = @()
  if ($Mode -eq 'cached') { $CacheArg = @('--cache') }
  & $SparkSubmit --master 'local-cluster[2,1,1024]' (Join-Path $Root 'src\run_pagerank.py') --input (Join-Path $Root 'data\sample_edges.txt') --output $Output --iterations 6 --partitions 4 --write-ranks @CacheArg
}
& $Python (Join-Path $Root 'src\verify_correctness.py') --input (Join-Path $Root 'data\sample_edges.txt') --spark-results (Join-Path $Root 'results\demo_cached.json') --iterations 6
