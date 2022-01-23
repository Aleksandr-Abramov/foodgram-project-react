from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (DockTemplate, FavoriteAPIView, FollowCreateDelete,
                    IngredientViewSet, RecipeViewSet, ShoppingCartAPIView,
                    ShoppingCartDownloadsAPIView, ShowListUserFollow,
                    TagsViewSet,) #UserIdViewSet)

router = DefaultRouter()
router.register("recipes", RecipeViewSet,)
router.register("tags", TagsViewSet,)
router.register("ingredients", IngredientViewSet,)
# router.register("user", UserIdViewSet,)


urlpatterns = [
    path("recipes/download_shopping_cart/",
         ShoppingCartDownloadsAPIView.as_view()),
    path("recipes/<int:recipe_id>/favorite/",
         FavoriteAPIView.as_view()),
    path("recipes/<int:recipe_id>/shopping_cart/",
         ShoppingCartAPIView.as_view()),
    path("users/<int:author_id>/subscribe/",
         FollowCreateDelete.as_view()),
    path("users/subscriptions/",
         ShowListUserFollow.as_view()),

    path("docs/", DockTemplate.as_view()),
    path("", include(router.urls)),
]
