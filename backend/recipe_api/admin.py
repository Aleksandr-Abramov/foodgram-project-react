# from django.contrib import admin
#
# from .models import (Follow,
#                      Recipe,
#                      RecipeIngredient,
#                      Tag, Ingredient,
#                      Favorite, ShoppingCart)
#
#
# admin.site.register(Follow)
# admin.site.register(Recipe)
# admin.site.register(RecipeIngredient)
# admin.site.register(Tag)
# admin.site.register(Ingredient)
# admin.site.register(Favorite)
# admin.site.register(ShoppingCart)
from django.contrib import admin

# from .models import Recipe, Ingredient, Tag, ShoppingCart, Favorite
from .models import (Favorite, Follow, Ingredient, Recipe, RecipeIngredient,
                     ShoppingCart, Tag)


# admin.site.register(Recipe)
@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    fields = ('author',
              'name',
              'image',
              'text',
              'cooking_time',
              'tags',
              'ingredients',
              )
    readonly_fields = (
        'pub_date',
    )
    empty_value_display = '-пусто-'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    fields = (
        'name',
        'measurement_unit'
    )
    search_fields = (
        'name',
    )
    empty_value_display = '-пусто-'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    fields = (
        'name',
        'color',
        'slug'
    )
    empty_value_display = '-пусто-'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'recipe',
        'added_date'
    )
    search_fields = (
        'user',
        'recipe'
    )


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'recipe',
        'added_date'
    )
    search_fields = (
        'user',
        'recipe'
    )
