from django.contrib import admin
from sale.models import Customer, Sale, Invoice, CostOfSale

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'address')
    
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('date', 'teller', 'customer', 'amount', 'discount')
    search_fields = ('teller', 'customer')

class SaleAdmin(admin.ModelAdmin):
    list_display = ('item', 'invoice', 'price', 'quantity')
    search_fields = ('item__name', 'item__code')

class CostOfSaleAdmin(admin.ModelAdmin):
    list_display = ('sale', 'amount')
    
    def has_add_permission(self, request):
        return False
    
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Sale, SaleAdmin)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(CostOfSale, CostOfSaleAdmin)
