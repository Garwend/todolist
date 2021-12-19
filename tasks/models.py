from django.db import models


class Task(models.Model):
    title = models.CharField(max_length=255)
    done = models.BooleanField(default=False)
    author_ip = models.GenericIPAddressField()
    created_date = models.DateTimeField(auto_now_add=True)
    done_date = models.DateTimeField(null=True, blank=True)
