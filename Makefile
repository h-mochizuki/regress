#
#       Makefile for Docker build.
# !! Use make.bat, if you are in Windows !!
#
NAME=regress
TAG=0.1
MARK=""

update:
	docker build --build-arg UPDATE_LOCK=1 --no-cache -t ${NAME}:${TAG} .
	docker run --rm -it -p 5000:5000 ${NAME}:${TAG} pip freeze > requirements.lock

lock:
	docker build -t ${NAME}:${TAG} .
	docker run --rm -it -p 5000:5000 ${NAME}:${TAG} pip freeze > requirements.lock

test:
	docker build --build-arg DEPENDENCIES=requirements_dev.txt -t ${NAME}:${TAG} .
	docker run --rm -it -p 5000:5000 ${NAME}:${TAG} pytest -v -m ${MARK}
	docker run --rm -it -p 5000:5000 ${NAME}:${TAG} python -m flake8 --max-line-length=100

local:
	pip install --no-cache-dir -r requirements.txt
	pip install --no-cache-dir -r requirements_dev.txt
	python setup.py test

hub:
	docker-compose up
	docker-compose down
	docker system prune -f

clean:
	python setup.py clean --all
	docker system prune

build:
	python setup.py sdist
	python setup.py clean --all
