### Coin Data Scrapping

#### Tech Used Selenium, BeautifulSoup, Django Rest Framework, Celery, Redis

### How to run on your machine

You need to have docker installed on your machine

Run the following Command
`docker-compose up -d --build`

### API Endpoints,

Gives you the Data scraped
GET http://localhost:8000/api/scrap?task_id=

POST http://localhost:8000/api/scrap
