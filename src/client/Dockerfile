FROM python:3.12

WORKDIR /app

COPY client.py /app/
COPY video_player.py /app/
COPY requirements.txt /app/

# Install server dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

EXPOSE 1234

# Command to run the server
CMD ["python", "-u", "client.py"]