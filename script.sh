#!/bin/bash

# Configuration
SERVICE_NAME="laravel-backend" # Name of the Laravel backend service (update as necessary)
CHECK_INTERVAL=300           # Time interval in seconds between checks
CPU_THRESHOLD=80            # CPU usage threshold percentage

# Function to get CPU usage as an integer
get_cpu_usage() {
    top -b -n2 | grep "Cpu(s)" | tail -n1 | awk '{print $2 + $4}' | cut -d'.' -f1
}

# Function to restart the Laravel service
restart_service() {
    echo "[$(date)] CPU usage is high: $CPU_USAGE%. Restarting $SERVICE_NAME..."
    systemctl restart $SERVICE_NAME
    if [ $? -eq 0 ]; then
        echo "[$(date)] Service $SERVICE_NAME restarted successfully."
    else
        echo "[$(date)] Failed to restart service $SERVICE_NAME."
    fi
}

# Periodically check CPU usage
while true; do
    CPU_USAGE=$(get_cpu_usage)

    if [ "$CPU_USAGE" -gt "$CPU_THRESHOLD" ]; then
        restart_service
    else
        echo "[$(date)] CPU usage is normal: $CPU_USAGE%. No action needed."
    fi

    sleep $CHECK_INTERVAL
done
