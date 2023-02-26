FROM python:slim-buster

WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN mkdir /var/log/gunicorn

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1  


EXPOSE 8000 

CMD ["gunicorn", "-c", "config/gunicorn/gunicorn.conf.py"]