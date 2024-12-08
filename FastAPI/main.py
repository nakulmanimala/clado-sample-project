#!/home/nakul/Desktop/clado-sample-project/venv/bin/python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import pika
import json
import os
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

if __name__ == "__main__":
    uvicorn.run(app, host=API_HOST, port=API_PORT)
