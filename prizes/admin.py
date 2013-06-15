from django.contrib.admin import site, ModelAdmin
from models import *

class WinnerAdmin(ModelAdmin):
    list_display = ["key","name","email"]

site.register(Winner,WinnerAdmin)