from decimal import Decimal
from django.shortcuts import render, redirect
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from rest_framework.decorators import action
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from django.db import transaction

from finance_app.mixins import SerializerMixin
from credits.models import Credit
from credits.serializers import CreditCreateSerializer, CreditSerializer
from credits.forms import CreditForm

class CreditsViewSet(mixins.ListModelMixin,
                     GenericViewSet):
    
    queryset = Credit.objects.all()
    
    permission_classes = [IsAuthenticated]
    
    serializer_class = CreditSerializer
    
    def list(self, request, *args, **kwargs):
        '''list of all credits assigned to user'''
        user = request.user
        queryset = Credit.objects.filter(bank_account__in=(user.bank_account, user.saving_account))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        context = {"credits": serializer.data}
        return render(request, "credits.html", context=context)
    
    
    @transaction.atomic
    @action(methods=["GET", "POST"], detail=False, url_path="request_credit")
    def request_credit(self, request: HttpRequest):
        '''create a credit instance with parameters specified in request.body'''
        context = {}
        if request.method == "GET":
            form = CreditForm()
            context['form'] = form
            return render(request, "request_credit.html", context=context)
        user = request.user
        password = str(request.POST.get('password'))
        total_sum = Decimal(request.POST.get('total_sum'))
        persent = float(request.POST.get('persent'))
        access_key = int(request.POST.get('access_key'))
        period = int(request.POST.get("period"))
        is_differential = str(request.POST.get('is_differential')) == 'on'
        if not (authenticate(request=request, email=user.email, password=password) and user.access_key == access_key):
            return HttpResponseBadRequest("Not valid password or access key")
        with transaction.atomic():
            Credit.objects.create(total_sum=total_sum, persent=persent, bank_account=user.bank_account, is_differential=is_differential, period=period)
            user.bank_account.balance += total_sum
            user.bank_account.save()
        return redirect("/credits/")
