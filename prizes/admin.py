from django.contrib.admin import site, ModelAdmin
from models import *

class WinnerAdmin(ModelAdmin):
    list_display = ["key","name","email","authentication_ip","authentication_time"]
    search_fields = ["key","name","email","authentication_ip","details_ip"]
    date_hierarchy = "authentication_time"

site.register(Winner,WinnerAdmin)