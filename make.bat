@echo off
if "%1"=="test-unit" (
  python -m unittest discover -s tests/unit -p "test_*.py"
  exit /b %ERRORLEVEL%
)
if "%1"=="smoke-env-bootstrap" (
  python scripts\probe_dependencies.py --json
  exit /b %ERRORLEVEL%
)
echo unsupported target: %1
exit /b 2
