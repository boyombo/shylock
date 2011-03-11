from django.db import models
from django.contrib.auth.models import User
from supplier.models import Supplier
from stock.models import Item
from datetime import datetime
from extras.daterange import MyDateField

class Reception(models.Model):
    item = models.ForeignKey(Item)
    supplier = models.ForeignKey(Supplier)
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
#
#class Transfer(models.Model):
#    item = models.ForeignKey(Item)
#    quantity = models.FloatField()
#    from_location = models.ForeignKey(Location, related_name='transfer_from')
#    to_location = models.ForeignKey(Location, related_name='transfer_to')
#    date = models.DateField(default=datetime.now)
#    user = models.ForeignKey(User, editable=False)
#
#    class Meta:
#        ordering = ('-date',)
