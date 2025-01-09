# Start with a base Python image.
FROM python:3.10-slim

# Set environment variables for Python image.
# Set PYTHONUNBUFFERED to non-zero so we get direct, unbuffered log outputs to the console.
ENV PYTHONUNBUFFERED 1
# Make Debian choose the default answers for prompts.
ENV DEBIAN_FRONTEND noninteractive

# Install ffmpeg so we can access the internet radio stream.
RUN apt-get update && apt-get install -y ffmpeg && apt-get clean

# Set a working directory
WORKDIR /app

# Copy the bot script and requirements
COPY bot.py /app/bot.py
COPY requirements.txt /app/requirements.txt

# Install our specified Python requirements
RUN pip install --no-cache-dir -r /app/requirements.txt

# Entrypoint
CMD ["python", "bot.py"]
