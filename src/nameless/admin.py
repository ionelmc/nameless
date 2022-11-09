from django.contrib import admin
from django.contrib.admin import register

from .models import Stuff


@register(Stuff)
class StuffAdmin(admin.ModelAdmin):
    pass
