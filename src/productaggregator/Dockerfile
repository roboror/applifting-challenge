FROM python:3.8
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "/usr/src/app"
WORKDIR /usr/src/app

ENV FLASK_ENV "production"
ENV FLASK_APP "app:create_app('ProductionConfig')"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["./docker-run.sh"]
