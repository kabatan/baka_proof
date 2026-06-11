@echo off
if "%1"=="test-unit" (
  python -m unittest discover -s tests/unit -p "test_*.py"
  exit /b %ERRORLEVEL%
)
echo unsupported target: %1
exit /b 2
