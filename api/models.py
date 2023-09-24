from django.db import models
import uuid
from datetime import timedelta

# Create your models here.
class Users(models.Model):
    id = models.AutoField(primary_key=True)
    uuid= models.CharField(max_length=255)
    name=models.CharField(max_length=100)
    email=models.CharField(max_length=45)
    annual_income=models.IntegerField(10)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    

class CreditScore(models.Model):
    id = models.AutoField(primary_key=True)
    user= models.ForeignKey(Users, on_delete=models.CASCADE, null=True)
    credit_score= models.IntegerField(10)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    
class LoanApplications(models.Model):
    id=models.AutoField(primary_key=True)
    user=models.ForeignKey(Users, on_delete=models.CASCADE)
    loan_id=models.CharField(max_length=50)
    loan_type=models.CharField(max_length=20, choices=[('car', 'Car'), ('home', 'Home'), ('education', 'Education'), ('personal', 'Personal')])
    loan_amount=models.DecimalField(max_digits=20, decimal_places=2)
    interest_rate=models.DecimalField(max_digits=5, decimal_places=2)
    term_period=models.IntegerField()
    disbursment_date=models.DateField()
    next_due_date=models.DateField()
    emi_amount=models.DecimalField(max_digits=20, decimal_places=2)
    outstanding_principal=models.DecimalField(max_digits=20, decimal_places=2)
    status=models.CharField(max_length=10, default='PENDING') # PENDING, ACTIVE, CLOSED
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    

class Transactions(models.Model):
    id=models.AutoField(primary_key=True)
    transaction_id=models.UUIDField(default=uuid.uuid4)
    loan=models.ForeignKey(LoanApplications, on_delete=models.CASCADE) #loan_id
    amount=models.DecimalField(max_digits=10, decimal_places=2)
    interest=models.DecimalField(max_digits=10, decimal_places=2)
    principal=models.DecimalField(max_digits=10, decimal_places=2)
    emi_date=models.DateField(null=True)
    transaction_type=models.CharField(max_length=10, choices=[('CREDIT', 'CREDIT'), ('DEBIT', 'DEBIT')], default='CREDIT')
    created_at=models.DateTimeField(auto_now_add=True)
    