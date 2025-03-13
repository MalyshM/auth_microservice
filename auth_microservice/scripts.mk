IMAGE_NAME = auth-microservice
CONTAINER_NAME = auth-microservice-container

SHELL = /bin/bash

# scripts
test:
	./auth_microservice/scripts/test.sh

check: 
	./auth_microservice/scripts/ruff_mypy.sh

format: 
	./auth_microservice/scripts/format.sh

# local start
start:
	uvicorn auth_microservice.src.main:app --host 0.0.0.0 --port 8090 --reload --forwarded-allow-ips='*' --proxy-headers
# create ssl cert and run
start_tls:
	uvicorn auth_microservice.src.main:app --host 0.0.0.0 --port 8090 --reload --forwarded-allow-ips='*' --proxy-headers --ssl-keyfile key.pem --ssl-certfile cert.pem

# Docker
build:
	docker build -t $(IMAGE_NAME) -f .Dockerfile .

run:
	make remove-if
	docker run --name $(CONTAINER_NAME) -p 8090:8090 $(IMAGE_NAME)

run-d:
	make remove-if
	docker run -d --name $(CONTAINER_NAME) -p 8090:8090 $(IMAGE_NAME)

stop:
	docker stop $(CONTAINER_NAME)

remove-if:
	@if [ "$$(docker ps -aq -f name=$(CONTAINER_NAME))" ]; then \
		echo "Removing existing container: $(CONTAINER_NAME)"; \
		docker rm -f $(CONTAINER_NAME); \
	fi;

remove:
	docker rm $(CONTAINER_NAME)

start-stopped:
	docker start $(CONTAINER_NAME)