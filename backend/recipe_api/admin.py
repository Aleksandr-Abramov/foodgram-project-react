from django.contrib import admin

from .models import (Favorite, Follow, Ingredient, Recipe, RecipeIngredient,
                     ShoppingCart, Tag)


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
    search_fields = (
        'name',
        'author__username',
        'tags__name',
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


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'recipe',
        'ingredient',
        'amount',
    )
    search_fields = (
        'name',
    )


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


@admin.register(Follow)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'user',
                    'author',
                    )
