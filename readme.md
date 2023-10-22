- TASK С1. (3 бали) MVC. Розробити систему, використовуючи MVC-підхід (в моделі 3+ сутностей зі зв’язками, одне з полів має бути типу файл (посилання) + реалізувати CRUD).
So, all the logic is inside the main.py file and all the tables are in models.py

- TASK С2. (2 бали) Cloud. Викласти проект в Інтернет використовуючи CSP (Azure або інше cloud-сховище: Heroku, DigitalOcean etc.). Рекомендовано скористатися @knu.ua адресою для отримання безкоштовного доступу до хмарних ресурсів:
We will use AWS, we go here 
https://eu-north-1.console.aws.amazon.com/ec2/home?region=eu-north-1#Instances:v=3;$case=tags:true%5C,client:false;$regex=tags:false%5C,client:false;sort=desc:publicIp
choose the instance, press connect -> using EC2 instance -> then go to folder and launch with uvicorn.
Then you print this
```
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000
```
and go to your public ip address. it should be ok.

- TASK C3. (2 бали) CI/CD. Налаштувати автоматичне розгортання проєкту у хмарному середовищі. Зміни в проєкті мають автоматично розгортатися після оновлення main-гілки в системі контролю версій. В якості платформи можна використати GitHub Actions, Azure DevOps, Azure WebApp Deployment та інші.
Just go to the pull requests and show the pull request CI

- TASK С4. (1 бал) Контейнеризація. Контейнеризувати проєкт у Docker-образ та використати його для розгортання проєкту у середовищі оркестрації контейнерів (Docker Compose, Kubernetes). Розгортання може бути виконано локально.
You can print 
```
docker-compose up
```
in the console and then go to localhost.

- TASK C5 (3 бали) JSON/XML (REST) API.
JSON file to insert into POSTMAN to add/change/delete CATEGORIES:
```
{
    "id": "3",
    "name": "aaa"
}
```
to add, we use `/createJSON_categories/` with above body
to change table, we use `/changeJSON_categories/`
and to delete we use `/deleteJSON_categories/` , every time provided with JSON BODIES
also added task b8 and c19, need to tell about all previous tasks

- TASK QA1. (2 бали) Автоматичне тестування Web API. Налаштувати середовище для тестування Web API для проєкту з C5 з використанням можливостей Postman, SOAP UI, або подібного ПЗ.
Take a look at the pytest, its automated testing framework.

- TASK C6. (3 бали) Bootstrap (Landing Page)
We have main page with all the items.

- TASK С7. (1 бал) SEO оптимізація сторінки.
![this is the seo result on my site](/templates/static/img/Seo_result.png)

- TASK QA2. (3 бали) E2E тестування.
Test file is `end2end_test.py` There I was testing creating and deleting random category

- TASK C8. (3 бали) Інтеграція зі сторонніми API. Скористатись стороннім API. 
I used gmaps api, when I open the details of news, I can see the map where it was.

- TASK F1. (2 бали) Візуалізація статистики.
I used ChartJS, its located on /chart [i took some random data and I also can append data to chart from db console]

- TASK F6. (4 бали) Графіка. 
I used js canvas to create a game. to open a game, right click on the html file and open file in browser

- TASK B4 (3 бали) Пошук.
To search something in news, we can go to /search and put some words there. Search engine is Whoosh.

- TASK C19 (3 бали) Статичний контент.
I put some files and images on s3 bucket, and we can access it just by typing `/s3_storage_image/{filename}`

- TASK B1. (2 бали) Pagination API. - below

- TASK F5. (3 бали) SPA.
I have an another directory SPA. We can use script to startup it (only locally) and go to localhost:3002 to see the site with pagination

- TASK QA3. (3 бали) Тестування процесу автентифікації/авторизації.
All the tests are running by pytest. There we create a user and authenticate him.

- TASK B6. (3 бали) Feature flags.
We have a function check_admin that permit specific access only for admins,.

- TASK B9. (3 бали) Кешування на рівні API.
As a cache storage I used Redis and for caching - external library called fastapi-cache2. I created a page that has a time-consumptive function and caches the result after executing. Cache lasts 15 seconds. To run redis locally we need to run `redis-cli` in another terminal.

- TASK B7. (3 бали) Serverless.
I put the minimal version of program on AWS Lambda. We can access it using link
https://ak47ucyrrj42c3qnx5zlijmghq0fxlig.lambda-url.eu-north-1.on.aws/
Firstly, dependencies was build using requirements, then we made zip file with dependencies and after we put our program on top
