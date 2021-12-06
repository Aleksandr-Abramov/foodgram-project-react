from django.contrib import admin

from .models import (Follow,
                     Recipe)


admin.site.register(Follow)
admin.site.register(Recipe)
