## SimplyLoan 
#### A loan management application



### Project Setup:
1. clone this repository to your local
2. install below packages
```
$ pip install django

$ pip install djangorestframework

$ pip install mysqlclient

$ pip install python-mysqldb

$ pip install pandas

```

### Set Database values:
###### set database credentials in simplyloan/settings.py file


### Run migration:
```
$ python manage.py makemigrations

$ python manage.py migrate
```

### Run project:
```
$ python manage.py runserver
```

Application will be start on http://127.0.0.1:8000 URL

## API Details:
### API Name: /api/register-user
Method: POST

**Request Payload**:
```
curl -X POST -H "Content-Type: application/json" \
    -d '{"uuid": "d425d4ba-82ba-4f05-974f-c28933f40bdf", "name": "Parag", "email": "parage@gmail.com", "annual_income": "250000"}' \
    http://127.0.0.1:8000/api/register-user
```

**Response**:
```
{
    "id": 16,
    "uuid": "d425d4ba-82ba-4f05-974f-c28933f40bdf",
    "name": "Parag",
    "email": "parage@gmail.com",
    "annual_income": 250000,
    "created_at": "2023-09-24T02:00:22.107713+05:30",
    "updated_at": "2023-09-24T02:00:22.107713+05:30"
}
```
