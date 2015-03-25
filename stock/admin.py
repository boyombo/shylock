from django.contrib import admin
from stock.models import Item, Category, Location, Stock, SerialItem


class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'type')


class StockAdmin(admin.ModelAdmin):
    list_display = ('item', 'location', 'quantity')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


class ItemAdmin(admin.ModelAdmin):
    list_display = ('code', 'description', 'category',
                    'quantity', 'cost_price', 'selling_price')
    search_fields = ('code', 'category')


class SerialItemAdmin(admin.ModelAdmin):
    list_display = ('category', 'serial_number', 'location', 'cost_price',
                    'selling_price', 'sale_date', 'customer')


admin.site.register(Stock, StockAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(SerialItem, SerialItemAdmin)
