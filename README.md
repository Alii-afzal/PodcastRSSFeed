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
+ Python

* ![Django](#092E20)(https://www.djangoproject.com/)
+ Django REST framework
+ RabbitMq
+ Docker
+ Celery
+ Django-CELERY-BEAT

## Getting Started
### Prerequisites

| Framework/Library | Version |
|---|---|
| Next.js | 13.0 |
| React | 18.2 |
| Vue.js | 3.2 |
| Angular | 14.2 |
| Svelte | 3.5 |
| Laravel | 9.0 |
| Bootstrap | 5.2 |
| jQuery | 3.6 |

.table {
  width: 100%;
  border-collapse: collapse;
}

.table th,
.table td {
  border: 1px solid black;
  padding: 5px;
}

.table th {
  background-color: #ccc;
}

## Built With

This section should list any major frameworks/libraries used to bootstrap your project. Leave any add-ons/plugins for
the acknowledgements section. Here are a few examples.

| Framework/Library | Version |
|---|---|
| Next.js | 13.0 |
| React | 18.2 |
| Vue.js | 3.2 |
| Angular | 14.2 |
| Svelte | 3.5 |
| Laravel | 9.0 |
| Bootstrap | 5.2 |
| jQuery | 3.6 |
