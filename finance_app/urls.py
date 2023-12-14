from django.contrib import admin
from django.template import loader
from django.shortcuts import redirect, render
from django.urls import path, include


urlpatterns = [
    path('', lambda request: render(request, "main.html")),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('accounts/', include('accounts.urls')),
    path('credits/', include('credits.urls'))
]
