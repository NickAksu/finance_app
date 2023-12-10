from rest_framework.routers import DefaultRouter
from django.urls import path, include

from credits import views

app_name = 'credits'

router = DefaultRouter()
router.register('', views.CreditsViewSet, basename='credits')

urlpatterns = [
    path('', include(router.urls))
]