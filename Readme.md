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
#
### API Name: /api/appply-loan
Method: POST

**Request Payload**:
```
curl -X POST -H "Content-Type: application/json" \
    -d '{"uuid": "d425d4ba-82ba-4f05-974f-c28933f40bdf", "loan_type": "Car", "loan_ammount": "450000", "interest-rate": "14","term_period":"36","disbursment_date":"2023-09-27"}' \
    http://127.0.0.1:8000/api/apply-loan
```
**Response**:
```
{
    "loan_id": "SLOOOOOOOOO1",
    "due_dates": [
        {
            "date": "2023-10-01",
            "amount": 15380
        },
        {
            "date": "2023-11-01",
            "amount": 15380
        },
        {
            "date": "2023-12-01",
            "amount": 15380
        },
        {
            "date": "2024-01-01",
            "amount": 15380
        },
        {
            "date": "2024-02-01",
            "amount": 15380
        },
        {
            "date": "2024-03-01",
            "amount": 15380
        },
        {
            "date": "2024-04-01",
            "amount": 15380
        },
        {
            "date": "2024-05-01",
            "amount": 15380
        },
        {
            "date": "2024-06-01",
            "amount": 15380
        },
        {
            "date": "2024-07-01",
            "amount": 15380
        },
        {
            "date": "2024-08-01",
            "amount": 15380
        },
        {
            "date": "2024-09-01",
            "amount": 15380
        },
        {
            "date": "2024-10-01",
            "amount": 15380
        },
        {
            "date": "2024-11-01",
            "amount": 15380
        },
        {
            "date": "2024-12-01",
            "amount": 15380
        },
        {
            "date": "2025-01-01",
            "amount": 15380
        },
        {
            "date": "2025-02-01",
            "amount": 15380
        },
        {
            "date": "2025-03-01",
            "amount": 15380
        },
        {
            "date": "2025-04-01",
            "amount": 15380
        },
        {
            "date": "2025-05-01",
            "amount": 15380
        },
        {
            "date": "2025-06-01",
            "amount": 15380
        },
        {
            "date": "2025-07-01",
            "amount": 15380
        },
        {
            "date": "2025-08-01",
            "amount": 15380
        },
        {
            "date": "2025-09-01",
            "amount": 15380
        },
        {
            "date": "2025-10-01",
            "amount": 15380
        },
        {
            "date": "2025-11-01",
            "amount": 15380
        },
        {
            "date": "2025-12-01",
            "amount": 15380
        },
        {
            "date": "2026-01-01",
            "amount": 15380
        },
        {
            "date": "2026-02-01",
            "amount": 15380
        },
        {
            "date": "2026-03-01",
            "amount": 15380
        },
        {
            "date": "2026-04-01",
            "amount": 15380
        },
        {
            "date": "2026-05-01",
            "amount": 15380
        },
        {
            "date": "2026-06-01",
            "amount": 15380
        },
        {
            "date": "2026-07-01",
            "amount": 15380
        },
        {
            "date": "2026-08-01",
            "amount": 15380
        },
        {
            "date": "2026-09-01",
            "amount": 15380
        }
    ]
}

```

#
### API Name: /api/make-payment
Method: POST

**Request Payload**:
```
curl -X POST -H "Content-Type: application/json" \
    -d '{"loan_id": "SLOOOOOOOOO1", "ammount": "15380",}' \
    http://127.0.0.1:8000/api/make-payment
```
#
**Response**:
```
{
    "message": "Payment successfully done!",
    "transaction_id": "1262ed2c-b6a8-4bd5-97c7-bdf79f44d5a4"
}
```
#
### API Name: /api/get-statement?loan_id=SLOOOOOOOOO1
Method: POST

**Response**:

```
 {
    "loan_id": "SLOOOOOOOOO1",
    "past_transactions": [
        {
            "date": "2023-10-01",
            "interest": "5250.00",
            "principal": "10130.00",
            "amount_paid": "15380.00"
        },
        {
            "date": "2023-11-01",
            "interest": "5132.00",
            "principal": "10248.00",
            "amount_paid": "15380.00"
        }
    ],
    "future_transactions": [
        {
            "date": "2023-12-01",
            "amount": 15380
        },
        {
            "date": "2024-01-01",
            "amount": 15380
        },
        {
            "date": "2024-02-01",
            "amount": 15380
        },
        {
            "date": "2024-03-01",
            "amount": 15380
        },
        {
            "date": "2024-04-01",
            "amount": 15380
        },
        {
            "date": "2024-05-01",
            "amount": 15380
        },
        {
            "date": "2024-06-01",
            "amount": 15380
        },
        {
            "date": "2024-07-01",
            "amount": 15380
        },
        {
            "date": "2024-08-01",
            "amount": 15380
        },
        {
            "date": "2024-09-01",
            "amount": 15380
        },
        {
            "date": "2024-10-01",
            "amount": 15380
        },
        {
            "date": "2024-11-01",
            "amount": 15380
        },
        {
            "date": "2024-12-01",
            "amount": 15380
        },
        {
            "date": "2025-01-01",
            "amount": 15380
        },
        {
            "date": "2025-02-01",
            "amount": 15380
        },
        {
            "date": "2025-03-01",
            "amount": 15380
        },
        {
            "date": "2025-04-01",
            "amount": 15380
        },
        {
            "date": "2025-05-01",
            "amount": 15380
        },
        {
            "date": "2025-06-01",
            "amount": 15380
        },
        {
            "date": "2025-07-01",
            "amount": 15380
        },
        {
            "date": "2025-08-01",
            "amount": 15380
        },
        {
            "date": "2025-09-01",
            "amount": 15380
        },
        {
            "date": "2025-10-01",
            "amount": 15380
        },
        {
            "date": "2025-11-01",
            "amount": 15380
        },
        {
            "date": "2025-12-01",
            "amount": 15380
        },
        {
            "date": "2026-01-01",
            "amount": 15380
        },
        {
            "date": "2026-02-01",
            "amount": 15380
        },
        {
            "date": "2026-03-01",
            "amount": 15380
        },
        {
            "date": "2026-04-01",
            "amount": 15380
        },
        {
            "date": "2026-05-01",
            "amount": 15380
        },
        {
            "date": "2026-06-01",
            "amount": 15380
        },
        {
            "date": "2026-07-01",
            "amount": 15380
        },
        {
            "date": "2026-08-01",
            "amount": 15380
        },
        {
            "date": "2026-09-01",
            "amount": 15380
        }
    ]
}   
```