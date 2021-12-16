from .models import Recipe
from django_filters import rest_framework as filters


class RecipeFilter(filters.FilterSet):
    tags = filters.CharFilter(field_name="tags__name")
    author = filters.CharFilter(field_name="author__username")

    class Meta:
        model = Recipe
        fields = ("tags", "author",)
