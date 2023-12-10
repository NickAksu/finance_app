from django.db import transaction

from accounts.models import Account
from users.models import User


def send_money_transactional(request_user, balance, account_id):
    target_account = Account.objects.get(account_id=account_id)
    with transaction.atomic():
        balance = save_money_to_saving_account(balance, target_account=target_account)
        request_user.bank_account.balance -= balance
        target_account.balance += balance
        target_account.save()
        request_user.bank_account.save()
        
def save_money_to_saving_account(sum, target_account):
    target_user = User.objects.get(bank_account=target_account)
    if target_user.saving_account.is_activated:
        persent = target_user.saving_account.saving_percent
        savings = sum*persent/100
        sum -= savings
        target_user.saving_account.balance += savings
        target_user.saving_account.save()
    return sum
        