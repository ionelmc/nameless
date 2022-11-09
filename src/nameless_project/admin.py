from django.conf import settings
from django.contrib.admin import AdminSite


class CustomAdminSite(AdminSite):
    site_header = f'Nameless_Project v{settings.PROJECT_VERSION}'
