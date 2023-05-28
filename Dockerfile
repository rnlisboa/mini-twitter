# Imagem base
FROM python:3.10


WORKDIR /app


COPY requirements.txt .


RUN pip install -r requirements.txt


COPY . .


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN python3 -m venv venv
RUN source venv/bin/activate
RUN python3 manage.py collectstatic --noinput

CMD python3 manage.py runserver 0.0.0.0:8000
