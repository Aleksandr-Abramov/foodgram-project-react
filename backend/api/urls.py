from django.contrib import admin
from django.urls import path, include

from .views import IndexPage

urlpatterns = [
    path('api/', IndexPage.as_view(), name='index')
]