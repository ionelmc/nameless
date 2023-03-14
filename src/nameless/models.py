from django.db import models


class Stuff(models.Model):
    def __str__(self):
        return f"Stuff(pk={self.pk})"
