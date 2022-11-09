import admin_utils
import django_rq.views
from django.conf import settings
from django.contrib.admin import AdminSite


class CustomAdminSite(AdminSite):
    site_header = f'Nameless_Project v{settings.PROJECT_VERSION}'


admin_utils.register_view(app_label="django_rq", model_name="RQ")(django_rq.views.stats)
