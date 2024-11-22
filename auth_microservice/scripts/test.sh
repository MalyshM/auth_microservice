echo -e '\033[31m >>> run coverage <<< \033[0m'
coverage run --source src -m pytest --junitxml=report.xml || { echo 'test coverage failed' ; exit 1; }
coverage report -m || { echo -e '\033[31m test failed \033[0m' ; exit 1; }
coverage xml -o coverage.xml || { echo '\033[31m test failed \033[0m' ; exit 1; }