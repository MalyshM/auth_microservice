# SHELL = /bin/bash
test:
	./auth_microservice/scripts/test.sh

start:
	uvicorn auth_microservice.src.main:app --host 0.0.0.0 --port 8090 --reload --forwarded-allow-ips='*' --proxy-headers