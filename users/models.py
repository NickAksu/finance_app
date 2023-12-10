from collections.abc import Iterable
from typing import Any
from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser, UserManager
from django.dispatch import receiver
from django.db.models.signals import pre_save

from accounts.models import Account


class CustomUserManager(UserManager):
    use_in_migrations = True
    
    def create_superuser(self, username: str = "u", email: str | None = "", password: str | None = "", **extra_fields: Any) -> Any:
        extra_fields["bank_account"] = Account.objects.create()
        return super().create_superuser(username, email, password, **extra_fields)
    
    def create_user(self, username: str, email: str | None = ..., password: str | None = ..., **extra_fields: Any) -> Any:
        extra_fields["bank_account"] = Account.objects.create()
        return super().create_user(username, email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    bank_account = models.ForeignKey(Account, on_delete=models.PROTECT, editable=False, blank=False, related_name="bank_account")
    saving_account = models.ForeignKey(Account, on_delete=models.PROTECT, editable=False, blank=False, related_name="saving_account")
    access_key = models.IntegerField(null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def save_base(self, raw: bool = ..., force_insert: bool = ..., force_update: bool = ..., using: str | None = ..., update_fields: Iterable[str] | None = ...) -> Any:
        try:
            a = self.bank_account
            b = self.saving_account
        except Exception:
            self.bank_account = Account.objects.create()
            self.saving_account = Account.objects.create()
        return super().save_base(raw, force_insert, force_update, using, update_fields)
    
    objects = CustomUserManager()
