FROM python:latest 

WORKDIR /code

COPY requirements.txt /code/

RUN pip install -U pip

RUN pip install -r requirements.txt

COPY . /code/

EXPOSE 8000

# RUN apt update

# RUN apt update && apt install gettext -y

# RUN apt-get update && apt-get install -y apt-transport-https

# RUN apt-get update && apt-get install -y gettext

CMD python manage.py makemigrations && \
    python manage.py migrate && \
    python manage.py runserver 0.0.0.0:8000
    
    # python manage.py collectstatic --no-input && \