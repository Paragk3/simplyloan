from simplyloan import settings
import pandas
from random import randrange
from api.models import LoanApplications, Users
from datetime import date, timedelta
from django.core.exceptions import ObjectDoesNotExist

LOAN_AMOUNT_BOUNDS={
    'Car': 750000,
    'Personal': 1000000,
    'Home': 8500000,
    'Education': 5000000,
}

csv_path = settings.BASE_DIR / 'accounts/transactions.csv'

def calculate_credit_score(uuid):
    
    df = pandas.read_csv(csv_path, sep=',')
    
    debit_entries = df[(df['user'] == uuid) & ( df['transaction_type'] == 'DEBIT')]
    credit_entries = df[(df['user'] == uuid) & ( df['transaction_type'] == 'CREDIT')]
    
    debit_sum = debit_entries["amount"].sum()
    credit_sum = credit_entries["amount"].sum()
    savings_balance = round(credit_sum - debit_sum)
    
    # Define credit score ranges
    min_credit_score = 300
    max_credit_score = 900

    # Define balance thresholds
    low_balance_threshold = 100000  # Rs. 1,00,000
    high_balance_threshold = 1000000  # Rs. 10,00,000

    # Calculate the credit score based on savings balance
    if savings_balance >= high_balance_threshold:
        credit_score = max_credit_score
    elif savings_balance <= low_balance_threshold:
        credit_score = min_credit_score
    else:
        # Calculate credit score based on the balance within the range
        balance_range = high_balance_threshold - low_balance_threshold
        credit_score_range = max_credit_score - min_credit_score
        balance_difference = savings_balance - low_balance_threshold

        # Calculate credit score increment per unit balance change
        credit_score_increment = credit_score_range / balance_range

        # Calculate the user's credit score within the range
        credit_score = min_credit_score + (balance_difference * credit_score_increment)

    return round(credit_score)


def check_account(uuid):
    df = pandas.read_csv(csv_path, sep=',')
    
    account_entry = df[df['user'] == uuid]
    
    if account_entry['user'].count() > 0:
        return True
    else:
        return False
    
    
    
def generate_loan_id():
    loan_id = get_loan_id()
    already_exists = LoanApplications.objects.filter(loan_id=loan_id).exists()
    if already_exists == False:
        return loan_id
    else:
        generate_loan_id()


def get_loan_id():
    prefix = "SL"
    number = randrange(1, 999)
    rd_str = str(number)
    with_padded = rd_str.rjust(10, "O")
    return prefix+with_padded

def get_user(uuid):
    try:
        user = Users.objects.get(uuid=uuid)
    except ObjectDoesNotExist:
        return None

    return user

def check_eligibility(users, loan_type, amount, credit_score, interate_rate, annual_income, disbursment_date):
    if credit_score < 450:
       return "Your credit score is low" 
    elif interate_rate < 14:
       return "Interest rate should be >=14%"
    elif annual_income < 150000:
       return "Annual income is low, should be >= 150000"
    elif amount > LOAN_AMOUNT_BOUNDS[loan_type]:
        return "Loan amount for "+loan_type+" loan application must be less than " + str(LOAN_AMOUNT_BOUNDS[loan_type])
    else:
        # dis_date = datetime.datetime.strptime(disbursment_date, "%Y-%m-%d").strftime("%Y-%m-%d")
        
        today = date.today()
        if today > disbursment_date:
            return "Disbursment date should be future date"
    
    if LoanApplications.objects.filter(user_id=users.id, loan_type=loan_type, status="ACTIVE").exists():
        return "You already have an active loan"
        
    return "SUCCESS"
   
        
def calculate_emi(p, r, n):
    r = r/(12*100)  
    emi = (p*r*pow(1+r,n))/(pow(1+r,n)-1) 
    return emi

def emi_due_dates(tenure, emi_amount, disbursment_date):
    
    emi_schedule = []
    current_date = disbursment_date
    
    for month in range(1, tenure+1):
        next_due_date = (current_date.replace(day=1) + timedelta(days=32)).replace(day=1)
        
        emi_schedule.append({
            "date": next_due_date.strftime("%Y-%m-%d"),
            "amount": round(emi_amount)
        })
        current_date = next_due_date
        
    return emi_schedule

def get_monthly_details(principal, emi_amount, interest_rate):
    monthly_rate=float("{0:.4f}".format(interest_rate/12))
    
    monthly_interest = (float(principal) * monthly_rate)/100 
    monthly_principal= float(emi_amount) - monthly_interest
    return round(monthly_interest), round(monthly_principal)