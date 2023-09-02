FROM python:3.10

ENV PYTHONUNBUFFERED=1

RUN mkdir -p /usr/src/app/

WORKDIR /app
COPY ./requirements.txt /app

RUN pip install --no-cache-dir -r requirements.txt

COPY ./ /app/
RUN python ./manage.py collectstatic --noinput

EXPOSE 8000
CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]
