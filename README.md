# RSS Feed Aggregator
We have a Django backend project for aggregating and managing RSS feeds. In this project, we write a parser for analyzing and selecting different RSS feeds from various sources, including APIs and custom XML feeds.
In costume parser, we are doing the below tasks:
+ Explore feed metadata, custom tags, and namespaces.
+ Implement advanced parsing techniques, including XML namespaces, and extract rich content.
In this project, we use Celery, Celery Beat, RabbitMQ, Docker, Elastic Search, and Logging.
Periodic Tasks:
+ We use Celery and Celery Beat for extracting and updating podcast automatically in a spesefic times.
RabbitMq:
+ We use RabbitMq to send notifications when the user login, registering and when an updating podcast we send a notification to who subscribed to a special podcast.
Docker:
+ In this project we use different tools so we use docker for managing this project in different systems and work easier with all tools together.
Logging and Elastic Search:
+ We use Elastic Search for showing and managing Loggings.
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
The first thing to do is to clone the repository:
```
git clone https://github.com/Alii-afzal/PodcastRSSFeed.git
cd PodcastRSSFeed 
```
Create a virtual environment to install dependencies in and activate it:
See the https://docs.python.org/3/library/venv.html
In Windows:
```
python -m venv env
env\Scripts\activate
```
Then install the dependencies:
```
(env)$ pip install -r requirements.txt
```
Once pip has finished downloading the dependencies:
```
python manage.py migrate
python manage.py createsuperuser
docker compose up -d --build
```
