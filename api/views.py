from django.shortcuts import render
from api.serializers import UsersSerializer, LoanApplicationsSerializer,PaymentSerializer
from rest_framework.decorators import api_view
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from api.models import Users, CreditScore, LoanApplications,Transactions
from . import utils
from datetime import date, datetime, timedelta
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view
# Create your views here.

@api_view(['POST'])
def register_user(request):
    
    user_data = JSONParser().parse(request)
    # print(user_data)
    user_serializer = UsersSerializer(data=user_data)
    if user_serializer.is_valid():
        user_exist = Users.objects.filter(uuid=user_data['uuid']).exists()
    
        if user_exist == False:
            valid_account = utils.check_account(user_data['uuid'])
            if valid_account == True:
                
                user_serializer.save()
                user_id = user_serializer.data['id']
                
                credit_score = utils.calculate_credit_score(user_data['uuid'])
                
                credit_score_model = CreditScore(user_id=user_id, credit_score=credit_score)
                credit_score_model.save()
                
                return JsonResponse(user_serializer.data, status=status.HTTP_200_OK)
            else:
                return JsonResponse({'message': 'User account not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return JsonResponse({'message': 'User account already exist'}, status=status.HTTP_200_OK)
        
    return JsonResponse(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
 

@api_view(['POST'])
def apply_loan(request):
    loan_data = JSONParser().parse(request)
    loan_serializer = LoanApplicationsSerializer(data=loan_data)
    if loan_serializer.is_valid():
        uuid = loan_serializer.validated_data['uuid']
        loan_type = loan_serializer.validated_data['loan_type']
        loan_amount = loan_serializer.validated_data['loan_amount']
        interest_rate = loan_serializer.validated_data['interest_rate']
        term_period = loan_serializer.validated_data['term_period']
        disbursment_date = loan_serializer.validated_data['disbursment_date']

        # validation uuid_user
        users = utils.get_user(uuid)
        
        if users != None:
            credit = CreditScore.objects.get(user_id=users.id)
            
            eligible = utils.check_eligibility(users, loan_type, loan_amount, credit.credit_score, interest_rate, users.annual_income, disbursment_date)
            
            if eligible=="SUCCESS":
                
                emi = utils.calculate_emi(loan_amount, interest_rate, term_period)
                
                total_interest = (emi * term_period) - loan_amount
                
                if emi <= ((users.annual_income/12)*60/100) and total_interest > 10000:
                    due_dates = utils.emi_due_dates(term_period, emi, disbursment_date)
                    
                    loan_application = LoanApplications(
                        user=users,
                        loan_id=utils.generate_loan_id(),
                        loan_type=loan_type,
                        loan_amount=loan_amount,
                        interest_rate=interest_rate,
                        term_period=term_period,
                        disbursment_date=disbursment_date,
                        outstanding_principal=loan_amount,
                        next_due_date=datetime.strptime(due_dates[0]['date'], '%Y-%m-%d'),
                        emi_amount=round(emi),
                        status="ACTIVE",       
                    )
                    
                    loan_application.save()
                    
                    resp = {
                        'loan_id': loan_application.loan_id,
                        'due_dates': due_dates,
                    }
                    
                    return JsonResponse(resp, status=status.HTTP_200_OK)
                else:
                    return JsonResponse({'message': 'Not eligible for loan'}, status=status.HTTP_400_BAD_REQUEST)                
                                
            else:
                return JsonResponse({'message': eligible}, status=status.HTTP_400_BAD_REQUEST) 
        else:
           return JsonResponse({'message': 'User uuid: ' + uuid + ' is not valid'}, status=status.HTTP_404_NOT_FOUND) 
    else:        
        return JsonResponse(loan_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def make_payment(request):
    
    payment_data = JSONParser().parse(request)
    payment_serializer = PaymentSerializer(data=payment_data)
    if payment_serializer.is_valid():
        loan_id = payment_serializer.validated_data['loan_id']
        amount = payment_serializer.validated_data['amount']
        
        test_date = '2023-10-01' # set date for testing
        if test_date != "":
            today = datetime.strptime(test_date, '%Y-%m-%d').strftime('%Y-%m-%d')
        else:
            today = date.today()
            
        
        try:
            loan = LoanApplications.objects.get(loan_id=loan_id)
        except ObjectDoesNotExist:
            return JsonResponse({"message":"Loan not found"}, status=status.HTTP_404_NOT_FOUND)
            
        if loan.status == 'CLOSED':
            return JsonResponse({"message":"Loan is already closed."}, status=status.HTTP_400_BAD_REQUEST)
        elif loan.status == 'PENDING':
            return JsonResponse({"message":"Loan is not active."}, status=status.HTTP_400_BAD_REQUEST)
        elif today != loan.next_due_date.strftime('%Y-%m-%d'):
            return JsonResponse({"message":"Payment can only be made on 1st of every month"}, status=status.HTTP_400_BAD_REQUEST)
        
        
        transaction = Transactions.objects.filter(loan_id=loan.id, emi_date=loan.next_due_date)
        
        if transaction.exists():
            return JsonResponse({"message":"Payment already paid"}, status=status.HTTP_400_BAD_REQUEST)
        
        
        monthly_interest, monthly_principal = utils.get_monthly_details(loan.outstanding_principal, loan.emi_amount, loan.interest_rate)
        
        outstanding_due = loan.outstanding_principal-monthly_principal
        
        
        transaction = Transactions.objects.create(
            loan_id=loan.id,
            amount=amount,
            interest=monthly_interest,
            principal=monthly_principal,
            emi_date=loan.next_due_date,
            transaction_type='CREDIT'
        )
        
        new_next_due_date = (loan.next_due_date.replace(day=1) + timedelta(days=32)).replace(day=1)
        
        loan.next_due_date = new_next_due_date
        loan.outstanding_principal=outstanding_due
        
        if outstanding_due < 0:
            loan.status = "CLOSED"
        
        loan.save()
        
        resp = {
           'message': 'Payment successfully done!',
           'transaction_id': transaction.transaction_id,
        }
                
        return JsonResponse(resp, status=status.HTTP_200_OK)
    else:
         return JsonResponse(payment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
        

@api_view(['GET'])
def get_statement(request):
    loan_id = request.GET['loan_id']
    
    if loan_id != "":
        try:
            loan = LoanApplications.objects.get(loan_id=loan_id)
        except ObjectDoesNotExist:
            return JsonResponse({"message":"Loan not found"}, status=status.HTTP_404_NOT_FOUND)
        
        emi_due_dates = []
        paid_emi=[]
        
        past_payments = Transactions.objects.filter(loan_id=loan.id).order_by('emi_date')
        
        for trans in past_payments:
            paid_emi.append({
                'date': trans.emi_date,
                'interest': trans.interest,
                'principal': trans.principal,
                'amount_paid': trans.amount,         
            })
            
        last_paid_date = past_payments[len(past_payments)-1].emi_date    
            
        emi_paid=len(past_payments)
        emi_remaining=loan.term_period-emi_paid
        
        if emi_remaining != 0:
            emi_due_dates = utils.emi_due_dates(emi_remaining, loan.emi_amount, last_paid_date)
            
            
        resp = {'loan_id':loan_id, 'past_transactions': paid_emi, 'future_transactions': emi_due_dates}
        
        return JsonResponse(resp, status=status.HTTP_200_OK)
    else:
        return JsonResponse({'message':'Loan_id required for statement'}, status=status.HTTP_400_BAD_REQUEST)  
    
    