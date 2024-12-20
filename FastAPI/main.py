#!/home/nakul/Desktop/clado-sample-project/venv/bin/python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import pika
import json
import os
import mysql.connector
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get environment variables from .env file
RABBITMQ_HOST = os.environ['RABBITMQ_HOST']
RABBITMQ_PORT = int(os.environ['RABBITMQ_PORT'])
RABBITMQ_USER = os.environ['RABBITMQ_USER']
RABBITMQ_PASS = os.environ['RABBITMQ_PASS'] 
RABBITMQ_QUEUE = os.environ['RABBITMQ_QUEUE']
API_HOST = os.environ['API_HOST']
API_PORT = int(os.environ['API_PORT'])
CORS_ORIGINS = os.environ['CORS_ORIGINS'].split(',')

# MySQL Configuration
MYSQL_HOST = os.environ['MYSQL_HOST']
MYSQL_USER = os.environ['MYSQL_USER']
MYSQL_PASSWORD = os.environ['MYSQL_PASSWORD']
MYSQL_DATABASE = os.environ['MYSQL_DATABASE']

# Create FastAPI instance
app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define data model
class FormData(BaseModel):
    name: str
    description: str

def get_db_connection():
    """Create and return MySQL database connection"""
    return mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE
    )

# RabbitMQ connection
def send_to_queue(message):
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=RABBITMQ_HOST,
            port=RABBITMQ_PORT,
            credentials=credentials
        )
    )
    channel = connection.channel()
    channel.queue_declare(queue=RABBITMQ_QUEUE)
    channel.basic_publish(
        exchange='',
        routing_key=RABBITMQ_QUEUE,
        body=json.dumps(message)
    )
    connection.close()

@app.post("/")
async def receive_data(data: FormData):
    message = {
        "name": data.name,
        "description": data.description
    }
    send_to_queue(message)
    return {"status": "success", "message": "Data received and sent to queue"}

@app.get("/data")
async def get_data():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT name, description FROM form_submissions")
        data = cursor.fetchall()
        return data
    except Exception as e:
        return {"error": str(e)}
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    uvicorn.run(app, host=API_HOST, port=API_PORT)
