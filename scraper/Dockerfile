# Use an official lightweight Python image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Install necessary dependencies
RUN apt-get update && apt-get install -y \
    cron \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the scraper script and database setup
COPY scraper.py /app/
COPY config.py /app/
COPY model.py /app/

# Copy the cron job definition
COPY cronjob /etc/cron.d/scraper_cron

# Give execution rights to the cron job
RUN chmod 0644 /etc/cron.d/scraper_cron

# Apply the cron job
RUN crontab /etc/cron.d/scraper_cron

# Start the cron service and keep the container running
CMD ["cron", "-f"]
