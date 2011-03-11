from django.db import models
from datetime import datetime

class Category(models.Model):
    name = models.CharField(max_length=100)
    
    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'categories'
    
    def __unicode__(self):
        return self.name
    
class Expense(models.Model):
    description = models.CharField(max_length=150)
    category = models.ForeignKey(Category, related_name='expenses')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(default=datetime.now)
    
    class Meta:
        ordering = ('date',)
    
    def __unicode__(self):
        return self.description