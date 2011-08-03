import models
from django.contrib import admin

class StationAdmin(admin.ModelAdmin):
  list_display = ('code','name')


admin.site.register(models.Station, StationAdmin)
