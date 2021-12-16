from django.contrib import admin

from .models import (Follow,
                     Recipe, RecipeIngredient, Tag, Ingredient, Favorite, ShoppingCart)


admin.site.register(Follow)
admin.site.register(Recipe)
admin.site.register(RecipeIngredient)
admin.site.register(Tag)
admin.site.register(Ingredient)
admin.site.register(Favorite)
admin.site.register(ShoppingCart)
