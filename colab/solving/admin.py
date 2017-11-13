from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from . import models

# Register your models here

class SolutionAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change)

admin.site.register(models.Exercice)
admin.site.register(models.Solution, SolutionAdmin)
admin.site.register(models.Category, MPTTModelAdmin)
