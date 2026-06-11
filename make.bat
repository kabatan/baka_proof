@echo off
if "%1"=="test-unit" (
  python -m unittest discover -s tests/unit -p "test_*.py"
  exit /b %ERRORLEVEL%
)
if "%1"=="test-mutation" (
  python -m unittest tests.unit.test_geometry_extraction tests.unit.test_target_subset
  exit /b %ERRORLEVEL%
)
if "%1"=="smoke-env-bootstrap" (
  python scripts\probe_dependencies.py --json
  exit /b %ERRORLEVEL%
)
if "%1"=="smoke-resource-governor" (
  python scripts\probe_local_resources.py --json
  exit /b %ERRORLEVEL%
)
if "%1"=="smoke-model-provider-set" (
  python scripts\smoke_model_provider_set.py
  exit /b %ERRORLEVEL%
)
if "%1"=="lean-build" (
  lake build
  exit /b %ERRORLEVEL%
)
if "%1"=="lean-no-sorry" (
  python scripts\check_lean_no_sorry.py
  exit /b %ERRORLEVEL%
)
if "%1"=="smoke-target-library-status" (
  python -m math_auto_research.cli.report_target_library_status
  exit /b %ERRORLEVEL%
)
if "%1"=="smoke-geometry-extraction" (
  python scripts\smoke_geometry_extraction.py
  exit /b %ERRORLEVEL%
)
echo unsupported target: %1
exit /b 2
