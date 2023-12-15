from datetime import date
from django.shortcuts import render, redirect
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import authenticate
from django.contrib import messages
from django.db import transaction
from django.http import HttpResponseBadRequest

from accounts.services import send_money_transactional, save_money_to_saving_account
from accounts.models import Account,Operation
from users.models import User
from accounts.serializers import AccountSerializer
from accounts.forms import PutMoneyForm, SendMoneyForm, LocalMoneyForm, ActivateSavingForm

class AccountViewSet(GenericViewSet):
    
    permission_classes = [IsAuthenticated]
    
    queryset = Account.objects.all()
    
    def list(self, request):
        accounts = User.objects.filter(id=request.user.id).values("bank_account", "saving_account").first()
        context = {"savings_account": Account.objects.get(account_id=accounts["saving_account"]), "bank_account": Account.objects.get(account_id=accounts["bank_account"]), "user": request.user}
        return render(request=request, template_name="accounts.html", context=context)
    
    serializer_class = AccountSerializer
    
    @action(methods=["POST", "GET"], detail=False, url_path="activate_account")
    @transaction.atomic
    def activate_account(self, request):
        if request.method == "POST":
            with transaction.atomic():
                request.user.saving_account.is_activated = True
                request.user.saving_account.saving_percent = request.POST.get("saving_percent")
                request.user.saving_account.save()
            return redirect("/accounts/")
        if request.user.saving_account.is_activated:
            with transaction.atomic():
                request.user.saving_account.is_activated = False
                request.user.saving_account.saving_percent = 0
                request.user.saving_account.save()
            return redirect("/accounts/")
        form = ActivateSavingForm()
        context = {"form": form}
        return render(request, "activate_account.html", context)
    
    @action(methods=["GET", "POST"], detail=False, url_path="put_money")
    @transaction.atomic
    def put_money(self, request):
        form = SendMoneyForm()
        context = {"form": form}
        if request.method == "POST":
            password = request.POST.get("password")
            access_key = int(request.POST.get("access_key"))
            if not (user := authenticate(request=request, email=request.user.email, password=password)):
                return HttpResponseBadRequest("Not valid password")
            if not request.user.access_key == access_key:
                messages.error(request=request, message="Invalid access key")
                return render(request=request, template_name="add_money.html", context=context)
            balance = int(request.POST.get("balance"))
            with transaction.atomic():
                if request.user.saving_account.is_activated:
                    balance = save_money_to_saving_account(sum=balance, target_account=user.bank_account)
                user.bank_account.balance += balance
                user.bank_account.save()
                Operation.objects.create(sender=user.bank_account, reciever=user.bank_account, sum_sent=balance)
                return redirect("/accounts/")
        if request.method == "GET":
            return render(request=request, template_name="add_money.html", context=context)
                
    @action(methods=["GET", "POST"], detail=False, url_path="send_money")
    @transaction.atomic
    def send_money(self,request):
        if request.method == "GET":
            form = SendMoneyForm()
            context = {"form": form}
            return render(request=request, template_name="send_money.html", context=context)
        if request.method == "POST":
            if request.user.bank_account.balance < int(request.POST.get("balance")):
                messages.error(request=request, message="You have not enough money")
                return render(request=request, template_name="send_money.html", context=context)
            password = request.POST.get("password")
            access_key = int(request.POST.get("access_key"))
            if authenticate(request=request, email=request.user.email, password=password) and request.user.access_key == access_key:
                balance = int(request.POST.get("balance"))
                account_id = request.POST.get("account_id")
                send_money_transactional(request_user=request.user, balance=balance, account_id=account_id)
                target_user = User.objects.get(bank_account__account_id=account_id)
                Operation.objects.create(sender=request.user.bank_account, reciever=target_user.bank_account, sum_sent=balance)
                return redirect("/accounts/")
            else:
                messages.error(request, "Password is incorrect")
            return render
        
        
    @action(methods=["GET",], detail=False, url_path="operations")
    def operatons(self, request):
        all_operations = Operation.objects.all()
        return render(request=request, template_name="operations.html", context={"operations": all_operations})
    
    @action(methods=["GET", "POST"], detail=False, url_path="add_from_saved")
    @transaction.atomic
    def add_from_saved(self, request):
        if request.method == "POST":
            user = request.user
            balance = int(request.POST.get('balance'))
            password = str(request.POST.get('password'))
            access_key = int(request.POST.get('access_key'))
            if not (authenticate(request, email=user.email, password=password) and user.access_key == access_key):
                return HttpResponseBadRequest("Not valid password or access_key")
            if user.saving_account.balance < balance:
                return HttpResponseBadRequest("Not enough money")
            with transaction.atomic():
                user.saving_account.balance -= balance
                user.saving_account.save()
                user.bank_account.balance += balance
                user.bank_account.save()
            return redirect("/accounts/")
        form = LocalMoneyForm()
        context = {"form": form}
        return render(request, "money_transfer.html", context)
            
