from django.contrib import admin

from .models import (Follow,
                     Recipe, RecipeIngredient, Tag, Ingredient)


admin.site.register(Follow)
admin.site.register(Recipe)
admin.site.register(RecipeIngredient)
admin.site.register(Tag)
admin.site.register(Ingredient)
