from django.contrib import admin

from . import models

# Register your models here.
admin.site.register(models.Client)
admin.site.register(models.Connection)
admin.site.register(models.Command)
admin.site.register(models.Result)
