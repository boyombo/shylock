from __future__ import unicode_literals

from django.db import models


class Supplier(models.Model):
    name = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=100, blank=True)
    address = models.TextField(blank=True)

    def __unicode__(self):
        return self.name
