from rest_framework.routers import DefaultRouter
from django.urls import path, include

from users import views

app_name = 'users'

router = DefaultRouter()
router.register('', views.UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
]