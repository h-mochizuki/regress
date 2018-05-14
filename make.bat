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
if "%env%"=="local" goto LOCAL
if "%env%"=="hub" goto HUB
if "%env%"=="clean" goto CLEAN
if "%env%"=="build" goto BUILD

:USAGE
    echo "USAGE"
    echo "$ %bat_name% <option>"
    echo "----"
    echo "option:"
    echo "    update:     Update dependencies."
    echo "    lock:       Lock dependencies."
    echo "    test:       Run tests on docker container."
    echo "    local:      Run tests on local."
    echo "    hub:        Start docker selenium-hub."
    echo "    clean:      Clean docker container and images."
    echo "    build:      Build project."
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

:LOCAL
    pip install --no-cache-dir -r requirements.txt
    pip install --no-cache-dir -r requirements_dev.txt
    python setup.py test
    goto EOF

:HUB
    set COMPOSE_CONVERT_WINDOWS_PATHS=1
    docker-compose up && docker-compose down && docker system prune -f
    goto EOF

:CLEAN
    python setup.py clean --all
    docker system prune -f
    goto EOF

:BUILD
    python setup.py sdist
    python setup.py clean --all
    goto EOF

:EOF
endlocal
