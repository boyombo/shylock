from django.db import models
from stock.models import Item
from datetime import datetime
from decimal import Decimal
from django.contrib.auth.models import User
from django.db.models import Max
from django.conf import settings

class Customer(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=50, blank=True)
    address = models.TextField(blank=True)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name

class InvoiceManager(models.Manager):
    @property
    def next_number(self):
        last_num = super(InvoiceManager, self).get_query_set().aggregate(Max('id'))['id__max']
        if not last_num:
            next_num = 1
        else:
            next_num = last_num + 1
        return unicode(next_num).zfill(settings.INVOICE_NUMBER_WIDTH)
    
class Invoice(models.Model):
    customer = models.ForeignKey(Customer, blank=True, null=True)
    date = models.DateField(default=datetime.now)
    discount = models.DecimalField(decimal_places=2, max_digits=10, default=Decimal("0.00"))
    teller = models.ForeignKey(User)
    
    objects = InvoiceManager()

    class Meta:
        ordering = ('-date',)

    def __unicode__(self):
        return '%s (%s)' % (self.date, self.amount)
    
    @property
    def invoice_number(self):
        return unicode(self.id).zfill(3)

    @property
    def amount(self):
        return sum(sale.amount for sale in self.sale_set.all()) - self.discount
    
class Sale(models.Model):
    item = models.ForeignKey(Item)
    quantity = models.FloatField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    invoice = models.ForeignKey(Invoice, null=True, blank=True)

    class Meta:
        ordering = ('-id',)
        
    def __unicode__(self):
        return '%s (%s)' % (self.item, self.quantity)
        
    def save(self):
        self.price = self.item.selling_price
        self.item.quantity -= self.quantity
        self.item.save()
        super(Sale, self).save()
    
    @property
    def amount(self):
        return Decimal(str(self.quantity)) * self.price

class CostOfSale(models.Model):
    sale = models.ForeignKey(Sale)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        ordering = ('sale__invoice__date',)
        
    def __unicode__(self):
        return self.amount

class Cart(models.Model):
    item = models.ForeignKey(Item, related_name="carts")
    qty = models.PositiveIntegerField(default=1)
    session_key = models.CharField(max_length=10)
    
    def __unicode__(self):
        return self.item.code
    