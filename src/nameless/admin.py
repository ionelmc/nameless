from admin_utils import register_view
from django.contrib import admin
from django.contrib.admin import register
from django_rq.stats_views import stats

from .models import Stuff

register_view(app_label="django_rq", model_name="RQ")(stats)


@register(Stuff)
class StuffAdmin(admin.ModelAdmin):
    pass
