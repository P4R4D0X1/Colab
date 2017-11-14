from django.contrib import admin
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin

from .models import Post, Category

admin.site.register(Post)
admin.site.register(Category, DraggableMPTTAdmin)
