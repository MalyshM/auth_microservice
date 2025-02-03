echo -e '\033[31m >>> run isort <<< \033[0m'
isort . --profile black || { echo -e '\033[31m isort failed \033[0m' ; exit 1; }
echo -e '\033[31m >>> run black <<< \033[0m'
black ./auth_microservice/src || { echo -e '\033[31m test black failed \033[0m' ; exit 1; }