from admin_utils import register_view
from django.contrib import admin
from django.contrib.admin import register
from django_rq import views

from .models import Stuff

register_view(app_label="django_rq", model_name="RQ")(views.stats)


@register(Stuff)
class StuffAdmin(admin.ModelAdmin):
    pass
