# SHELL = /bin/bash
test:
	./auth_microservice/scripts/test.sh

check: 
	./auth_microservice/scripts/ruff_mypy.sh

format: 
	./auth_microservice/scripts/format.sh

start:
	uvicorn auth_microservice.src.main:app --host 0.0.0.0 --port 8090 --reload --forwarded-allow-ips='*' --proxy-headers