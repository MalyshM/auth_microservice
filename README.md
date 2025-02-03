# Auth Microservice

This is an authentication microservice designed to handle user authentication and authorization. It is built with Python and uses PostgreSQL as the database.

---

## Prerequisites

Before starting the application, ensure you have the following installed:

- Python 3.9 or higher
- PostgreSQL
- `uv` (Python package manager)
- `make` (optional, for convenience)
- Docker (optional, for containerized deployment)

---

## Getting Started

Follow these steps to set up and run the application:

### 1. Set Up Environment Variables

Create a `.env` file in the root directory of the project and populate it with the required keys. Use the `.env.example` file as a template.

```bash
cp .env.example .env
```

Edit the `.env` file with your actual configuration values.

### 2. Install Dependencies

Install the required dependencies using `uv`:

```bash
uv sync
```
or
```bash
uv sync --group dev -U
```
### 3. Set Up Virtual Environment

Ensure you are using the correct Python interpreter. Activate the virtual environment (`.venv`):

```bash
source .venv/bin/activate  # On macOS/Linux
.venv\Scripts\activate     # On Windows
```

### 4. Initialize the Database

If you don't already have a database set up, run the following command to create it:

```bash
uv run auth_microservice/src/create_db.py
```

Make sure your PostgreSQL server is running and accessible.

### 5. Start the Application

Use the `make` command to start the application:

```bash
make start
```

Alternatively, you can start the application manually using the appropriate command for your setup.

---

## Docker

You can also run the application using Docker for containerized deployment.

### Build the Docker Image

```bash
docker build -t auth-microservice -f .Dockerfile .
```

### Run the Docker Container

To run the container in the foreground:

```bash
docker run --name auth-microservice-container -p 8090:8090 auth-microservice
```

To run the container in the background (detached mode):

```bash
docker run -d --name auth-microservice-container -p 8090:8090 auth-microservice
```

### Stop the Docker Container

```bash
docker stop auth-microservice-container
```
### Remove the Docker Container
```bash
docker rm auth-microservice-container
```
### Start a Stopped Container

To start a previously stopped container (replace `cc2b2afb4c9c` with your container ID):
```bash
docker start cc2b2afb4c9c
```
---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Submit a pull request with a detailed description of your changes.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Support

For any issues or questions, please open an issue on the [GitHub repository](https://github.com/MalyshM/auth_microservice).