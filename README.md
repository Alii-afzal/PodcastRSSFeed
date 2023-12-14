# RSS Feed Aggregator
We have a Django backend project for aggregating and managing RSS feeds. In this project, we write a parser for analyzing and selecting different RSS feeds from various sources, including APIs and custom XML feeds.

### In this project, we write a parser with python and use Celery, Celery Beat, RabbitMQ, Docker, ElasticSearch, Logging and Event Tracking.
#### In costume parser, we are doing the below tasks:
+ Explore feed metadata, custom tags, and namespaces.
+ Implement advanced parsing techniques, including XML namespaces, and extract rich content.
#### Periodic Tasks:
+ We use Celery and Celery Beat for extracting and updating podcast automatically in a spesefic times.
#### RabbitMq:
+ We use RabbitMq to send notifications when the user login, registering and when an updating podcast we send a notification to who subscribed to a special podcast.
#### Docker:
+ In this project we use different tools so we use docker for managing this project in different systems and work easier with all tools together.
#### ElasticSearch:
+ We store all update events and errors in an Elasticsearch database for monitoring and analysis.
#### Logging and Event Tracking:
+ We store every API request and response in one log.
+ We store Celery task actions and status changes in a dedicated log.
## Built With
+ DJANGO
+ DJANGO REST FRAMEWORK
+ RABBITMQ
+ DOCKER
+ REDIS
+ ELASTICSEARCH

## Getting Started
### Prerequisites
+ Python 3.11.5
+ Django 4.2.7

## Installation
1- The first thing to do is to clone the repository:
```
git clone https://github.com/Alii-afzal/PodcastRSSFeed.git
cd PodcastRSSFeed 
```
2- Create a virtual environment to install dependencies in and activate it:
See the https://docs.python.org/3/library/venv.html
In Windows:
```
python -m venv env
env\Scripts\activate
```
3- Create a .env file in your project root to store environment variables base on Django project settings like this:
```
SECRET_KEY= your secret key
DB_NAME= your postgres name
DB_USER= your postgres username
DB_PASSWORD= your postgres password
DB_HOST= your postgres host
DB_PORT= your postgres port

REDIS_HOST= your redis host
REDIS_PORT= your redis port

CELERY_BROKER= your celery broker url
CELERY_BACKEND= your celery backend url

RABBITMQ_HOST= your rabbitmq host
RABBITMQ_PORT= your rabbitmq port

ELASTICSEARCH_HOST= your elasticsearch host
ELASTICSEARCH_PORT= your elasticsearch port
```
4- Then install the dependencies:
```
(env)$ pip install -r requirements.txt
```
Congratulations! The RSS Feed Django project has been successfully set up on your machine.
## Running the Project
Once pip has finished downloading the dependencies:
```
python manage.py migrate
python manage.py createsuperuser
docker compose up -d --build
```
