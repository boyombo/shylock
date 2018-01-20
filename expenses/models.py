from __future__ import unicode_literals

from django.db import models
from datetime import datetime
from stock.models import Location


class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'categories'

    def __unicode__(self):
        return self.name


class Expense(models.Model):
    description = models.CharField(max_length=150)
    location = models.ForeignKey(Location, blank=True, null=True)
    category = models.ForeignKey(Category, related_name='expenses')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(default=datetime.now)

    class Meta:
        ordering = ('date',)

    def __unicode__(self):
        return self.description
