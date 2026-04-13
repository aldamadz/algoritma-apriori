@echo off
setlocal

cd /d %~dp0\..

if not exist venv (
  python -m venv venv
)

call venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements-notebook.txt

if not exist .jupyter_runtime mkdir .jupyter_runtime
if not exist .jupyter_config mkdir .jupyter_config
if not exist .jupyter_data mkdir .jupyter_data

set JUPYTER_RUNTIME_DIR=%cd%\.jupyter_runtime
set JUPYTER_CONFIG_DIR=%cd%\.jupyter_config
set JUPYTER_DATA_DIR=%cd%\.jupyter_data

python -m jupyter lab --ServerApp.use_redirect_file=False

endlocal
