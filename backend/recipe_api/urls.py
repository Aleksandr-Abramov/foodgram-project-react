from django.contrib import admin
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import (FollowCreateDelete,
                    ShowListUserFollow,
                    RecipeViewSet,)

from .views import DockTemplate

router = DefaultRouter()
router.register("recipes", RecipeViewSet,)



urlpatterns = [

    path("users/<int:author_id>/subscribe/", FollowCreateDelete.as_view()),
    path("users/subscriptions/", ShowListUserFollow.as_view()),
    path("docs/", DockTemplate.as_view()),
    path("", include(router.urls)),
]
