from django.contrib import admin
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import (FollowCreateDelete,
                    ShowListUserFollow,)

router = DefaultRouter()

from .views import DockTemplate

urlpatterns = [
    path("users/<int:author_id>/subscribe/", FollowCreateDelete.as_view()),
    path("users/subscriptions/", ShowListUserFollow.as_view()),
    path("docs/", DockTemplate.as_view())
]
