#!/usr/bin/env python
import pika
import json
import os
import sys
import mysql.connector
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Get environment variables from .env file
RABBITMQ_HOST = os.environ['RABBITMQ_HOST']
RABBITMQ_PORT = int(os.environ['RABBITMQ_PORT'])
RABBITMQ_USER = os.environ['RABBITMQ_USER']
RABBITMQ_PASS = os.environ['RABBITMQ_PASS']
RABBITMQ_QUEUE = os.environ['RABBITMQ_QUEUE']

# MySQL Configuration
MYSQL_HOST = os.environ['MYSQL_HOST']
MYSQL_USER = os.environ['MYSQL_USER'] 
MYSQL_PASSWORD = os.environ['MYSQL_PASSWORD']
MYSQL_DATABASE = os.environ['MYSQL_DATABASE']

def get_db_connection():
    """Create and return MySQL database connection"""
    return mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE
    )

def save_to_database(message):
    """Save message data to MySQL database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    sql = """INSERT INTO form_submissions (name, description, created_at) 
             VALUES (%s, %s, %s)"""
    values = (message['name'], message['description'], datetime.now())
    
    try:
        cursor.execute(sql, values)
        conn.commit()
        print("Data saved to database successfully")
    except Exception as e:
        print(f"Error saving to database: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def callback(ch, method, properties, body):
    """Callback function that processes received messages"""
    try:
        message = json.loads(body)
        print(f"Received message: {message}")
        save_to_database(message)
    except json.JSONDecodeError as e:
        print(f"Error decoding message: {e}")
    finally:
        ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    # Set up credentials and connection
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
    
    # Configure consumer
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(
        queue=RABBITMQ_QUEUE,
        on_message_callback=callback
    )
    
    print(f" [*] Waiting for messages in {RABBITMQ_QUEUE} queue. To exit press CTRL+C")
    channel.start_consuming()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
