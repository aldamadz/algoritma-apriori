$ErrorActionPreference = "Stop"

Set-Location (Join-Path $PSScriptRoot "..")

if (!(Test-Path "venv")) {
  python -m venv venv
}

& "venv\Scripts\activate"
python -m pip install --upgrade pip
python -m pip install -r requirements-notebook.txt

New-Item -ItemType Directory -Force -Path ".jupyter_runtime", ".jupyter_config", ".jupyter_data" | Out-Null

$env:JUPYTER_RUNTIME_DIR = "$PWD\.jupyter_runtime"
$env:JUPYTER_CONFIG_DIR = "$PWD\.jupyter_config"
$env:JUPYTER_DATA_DIR = "$PWD\.jupyter_data"

python -m jupyter lab --ServerApp.use_redirect_file=False
