FROM python:3.13.0

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

ENV NAME World

# Run app.py when the container launches
CMD ["python", "app.py"]