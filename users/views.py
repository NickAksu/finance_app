from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponseBadRequest, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from random import randint
from rest_framework.permissions import IsAuthenticated

from users.services import send_an_email
from users.forms import RegisterForm, LoginForm
from users.models import User
from users.serializers import UserBaseSerializer, UserMoneySerializer
from accounts.models import Account
from finance_app.mixins import SerializerMixin

class UserViewSet(SerializerMixin,
                  GenericViewSet,
                  ):

    permission_classes = []
    queryset = User.objects.all()
    
    serializer_class = UserBaseSerializer

    serializer_classes_for_actions = {
        "put_money": UserMoneySerializer,
    }
    
    def list(self, request, *args, **kwargs):
        '''list of all users'''
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        context = {"users": serializer.data}
        return render(request=request, template_name="users.html", context=context)
        
    @action(methods=["POST", "GET"], detail=False, url_path="register")
    def register(self, request: HttpRequest):
        """register user to application"""
        if request.method == "GET":
            form = RegisterForm()
            context = {'form': form, "name": "Registration"}
            return render(request, "registration.html", context)
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            print(f"\nemail: {user.email}", f"bank_account: {user.bank_account}\n", sep="\n")
            login(request=request, user=user)
        return redirect('/')
    
    @action(methods=["POST", 'GET'], detail=False, url_path='logout')
    def log_out(self, request):
        logout(request)
        return redirect('/')
    
    @action(methods=["POST", "GET"], detail=False, url_path="login", url_name="login")
    def _login(self, request: HttpRequest):
        '''login user to session if authentication is passed'''
        form = LoginForm()
        context = {'form': form, "name": "Login"}
        if request.method == "POST":
            email = request.POST.get("email")
            password = request.POST.get("password")
            access_key = request.POST.get("access_key")
            if user := authenticate(request=request, email=email, password=password):
                if int(access_key) == user.access_key:
                    login(request=request, user=user)
                    return redirect('/')
                else:
                    messages.error(request, "Incorrect access key")
            else:
                messages.error(request, "Incorrect Email or Password")
        return render(request, "login.html", context)
    
    @action(methods=["POST"], detail=False, url_path="code")
    def code(self, request: HttpRequest):
        """Creade an access_code and write it to db"""
        data = request.POST
        password = str(data['password'])
        email = request.POST.get('email') if not request.user.is_authenticated else request.user.email
        if user := authenticate(request=request, email=email, password=password):
            generated_code = randint(1000, 9999)
            user.access_key = generated_code
            user.save()
            send_an_email(subject="Access key", body=str(generated_code), send_to=email)
        else:
            return HttpResponseBadRequest("Not valid email or password")
        return JsonResponse({"status": 'key sended'}, status=200)
            
            
            
        
        