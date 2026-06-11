@echo off
if exist "%USERPROFILE%\.elan\bin\lean.exe" set "PATH=%USERPROFILE%\.elan\bin;%PATH%"
if "%1"=="test-unit" (
  python -m unittest discover -s tests/unit -p "test_*.py"
  exit /b %ERRORLEVEL%
)
if "%1"=="test-mutation" (
  python -m unittest tests.unit.test_geometry_extraction tests.unit.test_target_subset tests.unit.test_trace_compiler tests.unit.test_geotrace_rule_registry tests.unit.test_construction_compiler tests.unit.test_geometry_bridge tests.unit.test_final_verify
  exit /b %ERRORLEVEL%
)
if "%1"=="test-regression" (
  python -m unittest tests.unit.test_domain_contamination tests.unit.test_schema_validation tests.unit.test_target_library_status tests.unit.test_resource_governor tests.unit.test_composite_provider tests.unit.test_geometry_extraction tests.unit.test_trace_compiler tests.unit.test_geotrace_rule_registry tests.unit.test_construction_compiler tests.unit.test_geometry_bridge tests.unit.test_final_verify tests.unit.test_model_provider_set tests.unit.test_geometry_standard_loop tests.unit.test_run_trace
  if errorlevel 1 exit /b %ERRORLEVEL%
  python scripts\check_domain_contamination.py
  if errorlevel 1 exit /b %ERRORLEVEL%
  python scripts\check_no_loose_options.py
  exit /b %ERRORLEVEL%
)
if "%1"=="test-integration" (
  python -m unittest tests.unit.test_composite_provider tests.unit.test_geometry_standard_loop
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
  python scripts\smoke_leangeo_extraction.py
  exit /b %ERRORLEVEL%
)
if "%1"=="smoke-geometry-context-fixture" (
  python scripts\smoke_geometry_context_fixture.py
  exit /b %ERRORLEVEL%
)
if "%1"=="smoke-leangeo-fixture" (
  python scripts\check_leangeo_wsl_fixture.py
  exit /b %ERRORLEVEL%
)
if "%1"=="smoke-leangeo-extraction" (
  python scripts\smoke_leangeo_extraction.py
  exit /b %ERRORLEVEL%
)
if "%1"=="smoke-geometry-provider" (
  python scripts\smoke_geometry_provider.py
  exit /b %ERRORLEVEL%
)
if "%1"=="smoke-geometry-trace" (
  python scripts\smoke_geometry_trace.py
  exit /b %ERRORLEVEL%
)
if "%1"=="smoke-geometry-construction" (
  python scripts\smoke_geometry_construction.py
  exit /b %ERRORLEVEL%
)
if "%1"=="smoke-geometry-final-verify" (
  python scripts\smoke_geometry_final_verify.py
  exit /b %ERRORLEVEL%
)
echo unsupported target: %1
exit /b 2
