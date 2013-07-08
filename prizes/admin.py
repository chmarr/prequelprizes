from django.contrib.admin import site, ModelAdmin
from models import *

class WinnerAdmin(ModelAdmin):
    list_display = ["key","name","email","game_time","authentication_ip","authentication_time","details_time"]
    search_fields = ["key","name","email","authentication_ip","details_ip"]

site.register(Winner,WinnerAdmin)


class SettingAdmin(ModelAdmin):
    list_display = ["key","value"]
    list_editable = ["value"]

site.register(Setting,SettingAdmin)