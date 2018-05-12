@echo off
setlocal
rem =============================================
rem        Script for Docker build.
rem
rem !! Use Makefile, if you are not in Windows !!
rem =============================================
set project_home=%~dp0
set bat_name=%~nx0
set env=%1
set name=mkac_regression
set tag=0.1

if "%2"=="" (
    set mark=""
) else (
    set mark=%2
)

if "%env%"=="update" goto UPDATE
if "%env%"=="lock" goto LOCK
if "%env%"=="test" goto TEST
if "%env%"=="local_test" goto LOCAL_TEST
if "%env%"=="clean" goto CLEAN

:USAGE
    echo "USAGE"
    echo "$ %bat_name% <option>"
    echo "----"
    echo "option:"
    echo "    update:     Update dependencies."
    echo "    lock:       Lock dependencies."
    echo "    test:       Run tests on docker container."
    echo "    local_test:  Run tests on local."
    echo "    clean:      Clean docker container and images."
    goto EOF

:UPDATE
    docker build --build-arg UPDATE_LOCK=1 --no-cache -t %name%:%tag% .
    docker run --rm -it -p 5000:5000 %name%:%tag% pip freeze > requirements.lock
    goto EOF

:LOCK
    docker build -t %name%:%tag% .
    docker run --rm -it -p 5000:5000 %name%:%tag% pip freeze > requirements.lock
    goto EOF

:TEST
    docker build --build-arg DEPENDENCIES=requirements_dev.txt -t %name%:%tag% .
    docker run --rm -it -p 5000:5000 %name%:%tag% pytest -v -m %mark%
    docker run --rm -it -p 5000:5000 %name%:%tag% python -m flake8 --max-line-length=100
    goto EOF

:LOCAL_TEST
    pip install --no-cache-dir -r requirements.txt
    pip install --no-cache-dir -r requirements_dev.txt
    python src\setup.py test
    goto EOF

:CLEAN
    docker system prune -f
    goto EOF

:EOF
endlocal
