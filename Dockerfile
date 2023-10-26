FROM python:3.10.8

RUN mkdir /intergalactic_weather

WORKDIR /intergalactic_weather

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x docker/*.sh

# RUN alembic upgrade head

WORKDIR src

CMD gunicorn main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000