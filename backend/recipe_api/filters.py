from django_filters import rest_framework as filters

from .models import Ingredient, Recipe, Tag


class RecipeFilter(filters.FilterSet):
    tags = filters.CharFilter(
        field_name="tags__slug"
    )
    author = filters.CharFilter(
        field_name="author__id"
    )
    is_favorited = filters.BooleanFilter(
        method="get_favorite"
    )
    is_in_shopping_cart = filters.BooleanFilter(
        method="get_is_in_shopping_cart"
    )

    class Meta:
        model = Recipe
        fields = ("tags",
                  "author",
                  "is_in_shopping_cart",
                  "is_favorited"
                  )

    def get_favorite(self, queryset, name, value):
        if value:
            return Recipe.objects.filter(
                favorite_recipe__user=self.request.user
            )
        return Recipe.objects.all()

    def get_is_in_shopping_cart(self, queryset, name, value):
        if value:
            return Recipe.objects.filter(
                shopping_cart__user=self.request.user
            )
        return Recipe.objects.all()


class IngredientFilter(filters.FilterSet):
    name = filters.CharFilter(
        field_name='name',
        lookup_expr='icontains'
    )

    class Meta:
        model = Ingredient
        fields = ('name',)


class TagsFilter(filters.FilterSet):
    tags = filters.CharFilter(
        field_name="slug"
    )

    class Meta:
        model = Tag
        fields = ('tags',)


# class RecipeUserFilter(filters.FilterSet):
#     tags = filters.CharFilter(
#         field_name="tags__slug"
#     )
#     author = filters.CharFilter(
#         field_name="author__id"
#     )
#     is_favorited = filters.BooleanFilter(
#         method="get_favorite"
#     )
#     is_in_shopping_cart = filters.BooleanFilter(
#         method="get_is_in_shopping_cart"
#     )
#
#     class Meta:
#         model = Recipe
#         fields = ("tags",
#                   "author",
#                   "is_in_shopping_cart",
#                   "is_favorited"
#                   )
#
#     def get_favorite(self, queryset, name, value):
#         if value:
#             print(value)
#             return Recipe.objects.filter(
#                 favorite_recipe__user=self.request.GET.get("author")
#             )
#         return Recipe.objects.all()
#
#     def get_is_in_shopping_cart(self, queryset, name, value):
#         if value:
#             print(value)
#             return Recipe.objects.filter(
#                 shopping_cart__user__id=self.request.GET.get("author")
#             )
#         return Recipe.objects.all()
