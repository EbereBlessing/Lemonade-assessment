from dotenv import load_dotenv
import os
import time
import requests
from prometheus_client import start_http_server, Gauge

# Load environment variables from .env file
load_dotenv()

# Environment variables
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "guest")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD", "guest")
POLL_INTERVAL = int(os.getenv("POLL_INTERVAL", 15))
EXPORTER_PORT = int(os.getenv("EXPORTER_PORT", 8000))


# Prometheus metrics
rabbitmq_messages = Gauge(
    "rabbitmq_individual_queue_messages",
    "Total count of messages in RabbitMQ queue",
    ["host", "vhost", "queue"]
)
rabbitmq_messages_ready = Gauge(
    "rabbitmq_individual_queue_messages_ready",
    "Messages ready in RabbitMQ queue",
    ["host", "vhost", "queue"]
)
rabbitmq_messages_unacknowledged = Gauge(
    "rabbitmq_individual_queue_messages_unacknowledged",
    "Unacknowledged messages in RabbitMQ queue",
    ["host", "vhost", "queue"]
)

# RabbitMQ API base URL
API_BASE_URL = f"http://{RABBITMQ_HOST}:15672/api/queues"

def fetch_queue_data():
    """Fetch queue data from RabbitMQ HTTP API."""
    try:
        response = requests.get(API_BASE_URL, auth=(RABBITMQ_USER, RABBITMQ_PASSWORD))
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching data from RabbitMQ API: {e}")
        return []

def update_metrics():
    """Update Prometheus metrics."""
    queues = fetch_queue_data()
    for queue in queues:
        vhost = queue.get("vhost", "unknown")
        name = queue.get("name", "unknown")
        messages = queue.get("messages", 0)
        messages_ready = queue.get("messages_ready", 0)
        messages_unacknowledged = queue.get("messages_unacknowledged", 0)

        rabbitmq_messages.labels(host=RABBITMQ_HOST, vhost=vhost, queue=name).set(messages)
        rabbitmq_messages_ready.labels(host=RABBITMQ_HOST, vhost=vhost, queue=name).set(messages_ready)
        rabbitmq_messages_unacknowledged.labels(host=RABBITMQ_HOST, vhost=vhost, queue=name).set(messages_unacknowledged)

if __name__ == "__main__":
    # Start the Prometheus HTTP server
    start_http_server(EXPORTER_PORT)
    print(f"Starting Prometheus exporter on port {EXPORTER_PORT}")

    # Main loop
    while True:
        update_metrics()
        time.sleep(POLL_INTERVAL)
