FROM python:3.8

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app/

COPY app/requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt

COPY app /app/

EXPOSE 8000