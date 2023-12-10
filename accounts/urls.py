from rest_framework.routers import DefaultRouter
from django.urls import path, include

from accounts import views

app_name = 'accounts'

router = DefaultRouter()
router.register('', views.AccountViewSet, basename='accounts')

urlpatterns = [
    path('', include(router.urls)),
]