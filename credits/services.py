from datetime import date
from django.db import transaction

from credits.models import Credit
from accounts.models import Account

@transaction.atomic
def pay_all_credits():
    print("paying for credits")
    credits = Credit.objects.all()
    credits = [credit for credit in credits if credit.total_sum > credit.sum_payed]
    for credit in credits:
        with transaction.atomic():
            get_sum_to_pay(credit=credit)
                                    
                                    
def get_sum_to_pay(credit: Credit):
    if credit.is_differential:
        summ = is_differential_sum(credit=credit)
    else:
        summ = not_differential_sum(credit=credit)
    if credit.bank_account.balance < summ:
        return
    credit.bank_account.balance -= summ
    credit.sum_payed += summ
    credit.last_payed = date.today()
    credit.bank_account.save()
    credit.save()

def is_differential_sum(credit):
    return (credit.total_sum/credit.period) + ((credit.total_sum-credit.sum_payed)*credit.persent/100*30)/365 #30 дней в месяце и 365 дней в году
    
def not_differential_sum(credit):
    M = credit.persent/100/12
    return credit.total_sum * (M*(1+M)**credit.period)/((1+M)**(credit.period-1))