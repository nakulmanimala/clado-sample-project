# clado-sample-project

A sample project demonstrating integration between FastAPI, RabbitMQ, Celery, and MySQL. This project shows how to build a web API that receives form data, queues it using RabbitMQ, processes it with Celery workers, and stores it in a MySQL database.

## Features

- FastAPI web server for handling HTTP requests
- RabbitMQ message queue for task distribution
- Celery workers for background task processing
- MySQL database for data persistence


## Prerequisites

- Python 3.8 or higher
- MySQL Server 8.0+
- RabbitMQ Server 3.8+
- Docker (optional)
- Git

## Installation

### System Dependencies

First, install required system packages:

```bash
sudo apt-get update
sudo apt-get install python3-pip python3-dev default-libmysqlclient-dev build-essential pkg-config
```

### Python Environment Setup

Create and activate a Python virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # On Linux/Mac

Install required Python packages:

```bash
pip install -r requirements.txt
```

### Database Setup

Create a MySQL database and user:

```bash
mysql -u root -p
```

```sql
CREATE DATABASE clado_db;
CREATE USER 'clado_user'@'%' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON clado_db.* TO 'clado_user'@'%';
FLUSH PRIVILEGES;
```

### Environment Configuration FastAPI

Copy the example environment file and update it with your settings:

```bash
cp env_sample .env
```

Edit `.env` with your database credentials and other configurations:



## Running the Project

### Start Required Services

1. Start MySQL Server:
```bash
sudo service mysql start
```

2. Start RabbitMQ Server:
```bash
sudo service rabbitmq-server start
```

### Run the Application

1. Start the FastAPI server:
```bash
python FastAPI/main.py
```

2. Start Celery worker:
```bash
python Consumer/main.py
```

