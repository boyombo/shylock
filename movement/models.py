from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from supplier.models import Supplier
from stock.models import Item, Location, Stock
from datetime import datetime


class Reception(models.Model):
    item = models.ForeignKey(Item)
    supplier = models.ForeignKey(Supplier)
    location = models.ForeignKey(Location)
    #date = MyDateField()
    date = models.DateField()
    quantity = models.FloatField()
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ('-date',)

    def __unicode__(self):
        return '%s (%s)' % (self.item.description, self.item.code)

    def save(self):
        if not self.id:
            self.item.quantity += self.quantity
            self.item.cost_price = self.unit_cost
            self.item.save()

            # Add to stock for the location
            try:
                stock = Stock.objects.get(
                    item=self.item, location=self.location)
            except Stock.DoesNotExist:
                stock = Stock.objects.create(
                    item=self.item, location=self.location,
                    quantity=self.quantity)
            else:
                stock.quantity += self.quantity
                stock.save()
        super(Reception, self).save()

    def delete(self):
        if self.quantity > self.item.quantity:
            raise ValueError('Not enough stock')
        self.item.quantity -= self.quantity
        self.item.save()
        super(Reception, self).delete()


class Return(models.Model):
    item = models.ForeignKey(Item)
    supplier = models.ForeignKey(Supplier)
    date = models.DateField()
    quantity = models.PositiveIntegerField()

    class Meta:
        ordering = ('-date',)

    def __unicode__(self):
        return self.item.name

    def save(self):
        if not self.id:
            if self.quantity > self.item.quantity:
                raise ValueError('Not enough stock')
            self.item.quantity -= self.quantity
            self.item.save()
            super(Return, self).save()

    def delete(self):
        self.item.quantity += self.quantity
        self.item.save()
        super(Return, self).delete()


class Transfer(models.Model):
    item = models.ForeignKey(Item)
    quantity = models.FloatField()
    source = models.ForeignKey(Location, related_name='transfer_source')
    destination = models.ForeignKey(
        Location, related_name='transfer_destination')
    when = models.DateField(default=datetime.now)
    user = models.ForeignKey(User, editable=False)

    class Meta:
        ordering = ('-when',)
