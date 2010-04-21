from django.contrib import admin
from stock.models import Item, Category

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    
class ItemAdmin(admin.ModelAdmin):
    list_display = ('code', 'description', 'category', 'quantity', 'cost_price', 'selling_price')
    search_fields = ('code', 'category')
    
admin.site.register(Category, CategoryAdmin)
admin.site.register(Item, ItemAdmin)
