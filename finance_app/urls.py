from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include


urlpatterns = [
    path('', lambda request: redirect("/users/")),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('accounts/', include('accounts.urls')),
    path('credits/', include('credits.urls'))
]
