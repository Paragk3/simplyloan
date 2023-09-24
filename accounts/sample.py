import pandas
from random import uniform, randrange
from datetime import date,datetime, timedelta

def read_file(uuid):
    df = pandas.read_csv('transactions.csv', sep=',')
    
    debit_entries = df[(df['user'] == uuid) & ( df['transaction_type'] == 'DEBIT')]
    credit_entries = df[(df['user'] == uuid) & ( df['transaction_type'] == 'CREDIT')]
    print(credit_entries["user"].count())
    
    debit_sum = debit_entries["amount"].sum()
    credit_sum = credit_entries["amount"].sum()
    
    savings_balance = credit_sum - debit_sum
    
    # savings_balance = round(6668450)
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
        
        
    print("Debit Sum:", debit_sum)
    print("Credit Sum:", credit_sum)
    print("Saving Balance:", savings_balance)
    print("Credit_Score:", round(credit_score))
    
    
    
def check_account(uuid):
    df = pandas.read_csv('transactions.csv', sep=',')
    
    account_entries = df[df['user'] == uuid]
    print(account_entries['user'].count())
    
    if account_entries['user'].count() > 0:
        print("Account is Present")
    else:
        print("Account Is not Present")
  
  
def generate_uuid():
    number = randrange(1, 999)
    rd_str = str(number)
    with_padded = rd_str.rjust(10, "O")
    return "SL"+with_padded
    
    
def compare_date():
    input_d = "2023-09-24"
    
    today = str(date.today())
    print("Today:", today)
    print("Ddate:", input_d)
    
    if today <= input_d:
        print("Valid")
    else:
        print("Invalid")

def calculate_emi():
    p = 750000
    r = 14
    n = 36 
    r = r/(12*100)  
    emi = (p*r*pow(1+r,n))/(pow(1+r,n)-1) 
    print(emi) 


def next_month_date():
    today = date.today()
    # first_day = today.replace(day=1) + relativedelta(months=1)
    
    today = date.today()
    next_due_date = (today.replace(day=1) + timedelta(days=32)).replace(day=1)


def emi_due_dates(tenure, emi_amount, disbursment_date):
    
    emi_schedule = []
    # current_date = disbursment_date
    current_date = datetime.strptime(disbursment_date,'%Y-%m-%d')
    
    for month in range(1, tenure+1):
        next_due_date = (current_date.replace(day=1) + timedelta(days=32)).replace(day=1)
        
        emi_schedule.append({
            "date": next_due_date.strftime("%Y-%m-%d"),
            "amount": round(emi_amount)
        })
        current_date = next_due_date
        
    print(emi_schedule)

def monthly_interest():
    p = 450000
    r = 14
    n = 36
    monthly_rate="{0:.4f}".format(r/12)
    
    r = r/(12*100)  
    emi = (p*r*pow(1+r,n))/(pow(1+r,n)-1) 
    
    
    print("MonthlyRate:", monthly_rate)
    monthly_interest = (p*float(monthly_rate))/100 
    monthly_principal=emi-monthly_interest
    print("MonthlyInterest:", round(monthly_interest))
    print("MonthlyPrincipal:", round(monthly_principal))
    print("EMI:", round(emi))

if __name__ == '__main__':
    # read_file('61701abf-f3e0-4f10-9d81-cdadfb9c764f')
    # check_account('24fdd39c-f7f9-48f9-8fdd-93739e0d301e')
    # generate_uuid()
    # compare_date()
    # calculate_emi()
    # next_month_date()
    monthly_interest()
    # emi_due_dates(36, 15388, "2023-09-27")