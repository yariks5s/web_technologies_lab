С1. (3 бали) MVC. Розробити систему, використовуючи MVC-підхід (в моделі 3+ сутностей зі зв’язками, одне з полів має бути типу файл (посилання) + реалізувати CRUD).
So, all the logic is inside the main.py file and all the tables are in models.py

С2. (2 бали) Cloud. Викласти проект в Інтернет використовуючи CSP (Azure або інше cloud-сховище: Heroku, DigitalOcean etc.). Рекомендовано скористатися @knu.ua адресою для отримання безкоштовного доступу до хмарних ресурсів:
We will use AWS, we go here 
https://eu-north-1.console.aws.amazon.com/ec2/home?region=eu-north-1#Instances:v=3;$case=tags:true%5C,client:false;$regex=tags:false%5C,client:false;sort=desc:publicIp
choose the instance, press connect -> using EC2 instance -> then go to folder and launch with uvicorn.
Then you print this
```
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000
```
and go to your public ip address. it should be ok.

C3. (2 бали) CI/CD. Налаштувати автоматичне розгортання проєкту у хмарному середовищі. Зміни в проєкті мають автоматично розгортатися після оновлення main-гілки в системі контролю версій. В якості платформи можна використати GitHub Actions, Azure DevOps, Azure WebApp Deployment та інші.
Just go to the pull requests and show the pull request CI

С4. (1 бал) Контейнеризація. Контейнеризувати проєкт у Docker-образ та використати його для розгортання проєкту у середовищі оркестрації контейнерів (Docker Compose, Kubernetes). Розгортання може бути виконано локально.
You can print 
```
docker-compose up
```
in the console and then go to localhost.

TASK C5
JSON file to insert into POSTMAN to add/change/delete CATEGORIES:
{
    "id": "3",
    "name": "aaa"
}
to add, we use /createJSON_categories/ with above body
to change table, we use /changeJSON_categories/
and to delete we use /deleteJSON_categories/ , every time provided with JSON BODIES
also added task b8 and c19, need to tell about all previous tasks

QA1. (2 бали) Автоматичне тестування Web API. Налаштувати середовище для тестування Web API для проєкту з C5 з використанням можливостей Postman, SOAP UI, або подібного ПЗ.
Take a look at the pytest, its automated testing framework.

TASK C6. (3 бали) Bootstrap (Landing Page)
We have main page with all the items.

