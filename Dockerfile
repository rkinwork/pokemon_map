FROM python:3.7

EXPOSE 8000

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY . /app
RUN python manage.py migrate

ENTRYPOINT ["python","manage.py", "runserver"]