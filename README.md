# RateReviewRevive (API backend)
## _Media database for measterpiece art_
## based on:
[![N|Solid](https://static.djangoproject.com/img/logos/django-logo-negative.svg)](https://www.djangoproject.com/)
## and
[![N|Solid](https://www.django-rest-framework.org/img/logo.png)](https://www.django-rest-framework.org/)

RateReviewRevive is a joint project for learning, testing and improving skills on python, django, sql, REST api etc.


## Creators:
Kirill Svitsov
Leonid Martsinkevich
Sergei Baryshevskii

## Features
Does not contain web responses, html web pages rendering etc. It is projected to use with frontend module via SPA technology (using json exchange of data) or third-party app.

- Could start a DEV server
- Could containt information about media titles, reviews with scores and commentaries.

## Tech

RateReviewRevive uses a number of open source projects to work properly:

- [Python] - Python 3.9
- [Django] - Web framework to rule them all!
- [Django Rest Framework (DRF)] - REST API support for Django


RateReviewRevive on a [public repository][Rexant-b2k] on GitHub.

## Installation

RateReviewRevive requires [Django] v3.2.16 to run.

Install the dependencies and devDependencies and start the server (Linux/MacOS example).

```sh
cd ratereviewrevive
python -m pip install --upgrade pip
python -m venv venv
source venv/bin/activate
```

For production environments (automatic)...

```sh
pip install -r requirements.txt
```
or manual:
```sh
pip install Django==3.2.16
pip install djangorestframework
```

## Making migrations
```sh
python manage.py migrate
```

## Running server
```sh
python manage.py runserver
```

##### Information about possible request are available at **http://127.0.0.1:8000/redoc/ in your browser**

## Requests example
*Could be done using Postman or another simular app, or via browser.
###### Get posts list:
Request:
```HTTP
GET http://127.0.0.1:8000/api/v1/titles/
```
Response:

```JSON
{
  "count": 123,
  "next": "http://api.example.org/api/v1/titles/?offset=400&limit=100",
  "previous": "http://api.example.org/api/v1/titles/?offset=200&limit=100",
  "results": [
    {
      "id": 0,
      "name": "string",
      "year": 1985,
      "raiting": 5,
      "description": "string",
      "genre": [
        + {...}
        ],
      "category": {
        "name": "string",
        "slug": "string"
        },
    }
  ]
}
```

###### Make review:
Request:
```HTTP
POST http://127.0.0.1:8000/api/v1/title/{title_id}/reviews/
```
```JSON
{
    "text": "string",
    "score": 7
}
```

Response:
```JSON
{
    "id": 0,
    "text": "string",
    "author": "string",
    "score": 7,
    "pub_date": "2019-08-24T14:15:22Z"
}
```

## Plugins

RateReviewRevive is currently extended with the following plugins.
Instructions on how to use them in your own application are linked below.

| Plugin    | README         |
| ----------| -------------- |
| Dillinger | [Dillinger.io] |

## Docker

The information will be available in future.


## License

BSD-3 Clause License

**Free Software, Hello everybody**

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)

   [Rexant-b2k]: <https://github.com/Rexant-b2k>
   [git-repo-url]: <https://github.com/Rexant-b2k/RateReviewRevive.git>
   [Django]: <https://www.djangoproject.com>
   [Python]: <https://www.python.org/>
   [Django Rest Framework (DRF)]: <https://www.django-rest-framework.org/>
   [Dillinger.io]: <https://dillinger.io/>
