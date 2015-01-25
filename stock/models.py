from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Categories'

    def __unicode__(self):
        return self.name


class Item(models.Model):
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, null=True, blank=True)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ('category',)

    def __unicode__(self):
        return self.description


class Location(models.Model):
    SHOP = 0
    WAREHOUSE = 1
    LOCATION_TYPES = ((SHOP, 'Shop'), (WAREHOUSE, 'Warehouse'),)
    name = models.CharField(max_length=50, unique=True)
    type = models.PositiveIntegerField(choices=LOCATION_TYPES)

    def __unicode__(self):
        return self.name


class Stock(models.Model):
    item = models.ForeignKey(Item)
    location = models.ForeignKey(Location)
    quantity = models.PositiveIntegerField()

    def __unicode__(self):
        return unicode(self.item)


class UserAccount(models.Model):
    user = models.ForeignKey(User)
    location = models.ForeignKey(Location, null=True, blank=True)
    read_only = models.BooleanField()
    #active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.user.username
