
import datetime

from django.db import models
from django.utils import timezone

# Create your models here.
class Woeids(models.Model):
    country = models.CharField(max_length=200, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    woeid = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return '%s %s %s' % (
        self.country,
        self.name,
        str(self.woeid)
        )

