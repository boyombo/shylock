from django.db import models


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

#    def get_quantity(self):
#        qty = self.locationitems_set.aggregate(models.Sum('quantity'))
#        return qty['quantity__sum']
#    quantity = property(fget=get_quantity)
#
#class Location(models.Model):
#    SHOP = 0
#    WAREHOUSE = 1
#    LOCATION_TYPES = ((SHOP, 'Shop'),(WAREHOUSE, 'Warehouse'),)
#    name = models.CharField(max_length=50, unique=True)
#    type = models.PositiveIntegerField(choices=LOCATION_TYPES)
#    items = models.ManyToManyField(Item, through='LocationItems')
#
#    def __unicode__(self):
#        return self.name
#
#class LocationItems(models.Model):
#    item = models.ForeignKey(Item)
#    location = models.ForeignKey(Location)
#    quantity = models.FloatField()
#
#    class Meta:
#        verbose_name_plural = 'Stock'
#
#    def __unicode__(self):
#        return '%d units of %s at %s' % (self.quantity, self.item.name, self.location.name)
#
