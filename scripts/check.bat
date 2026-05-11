@echo off

echo ==================================
echo Running Black formatter...
echo ==================================
black .
IF %ERRORLEVEL% NEQ 0 EXIT /B %ERRORLEVEL%

echo ==================================
echo Running Black check...
echo ==================================
black --check .
IF %ERRORLEVEL% NEQ 0 EXIT /B %ERRORLEVEL%

echo.
echo ==================================
echo Running Ruff formatter...
echo ==================================
ruff format .
IF %ERRORLEVEL% NEQ 0 EXIT /B %ERRORLEVEL%

echo.
echo ==================================
echo Running Ruff check...
echo ==================================
ruff check .
IF %ERRORLEVEL% NEQ 0 EXIT /B %ERRORLEVEL%

echo.
echo ==================================
echo Running Pytest...
echo ==================================
pytest -v --tb=short --cov --cov-report=term-missing
IF %ERRORLEVEL% NEQ 0 EXIT /B %ERRORLEVEL%

echo.
echo ==================================
echo All checks passed!
echo ==================================
