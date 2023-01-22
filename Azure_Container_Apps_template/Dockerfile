FROM python:3.9
WORKDIR /app
COPY requirements.txt ./
RUN apt-get update
RUN pip install -r requirements.txt
COPY . /app
ENV PYTHONUNBUFFERED=1
RUN mkdir docker_bind
EXPOSE 5000
CMD [ "python", "app.py" ]