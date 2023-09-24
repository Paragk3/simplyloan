from api.models import Users, CreditScore
from rest_framework import serializers


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'uuid', 'name', 'email', 'annual_income', 'created_at', 'updated_at']
       

class CreditScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditScore
        fields = ['id', 'user_id', 'credit_score', 'created_at', 'updated_at']
        
class LoanApplicationsSerializer(serializers.Serializer):
    uuid= serializers.CharField(max_length=255)
    loan_type=serializers.ChoiceField(choices=[('Car', 'Car'), ('Home', 'Home'), ('Education', 'Education'), ('Personal', 'Personal')])
    loan_amount=serializers.DecimalField(max_digits=10, decimal_places=2)
    interest_rate=serializers.DecimalField(max_digits=5, decimal_places=2)
    term_period=serializers.IntegerField()
    disbursment_date=serializers.DateField()
    
class PaymentSerializer(serializers.Serializer):
    loan_id= serializers.CharField(max_length=255)
    amount=serializers.DecimalField(max_digits=10, decimal_places=2)
   
    

    