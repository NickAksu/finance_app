from typing import Any
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError

from users.models import User


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise ValidationError("An user with this email already exists!")
        return email
    

class LoginForm(forms.Form):
    email = forms.EmailField(max_length=150)
    password = forms.CharField(max_length = 150, widget=forms.PasswordInput)
