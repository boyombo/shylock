from django.contrib import admin
from movement.models import Reception, Return, Transfer


class ReceptionAdmin(admin.ModelAdmin):
    list_display = ('item', 'unit_cost', 'supplier', 'date')


class TransferAdmin(admin.ModelAdmin):
    list_display = (
        'item', 'quantity', 'source', 'destination', 'when', 'user')


admin.site.register(Reception, ReceptionAdmin)
admin.site.register(Return)
admin.site.register(Transfer, TransferAdmin)
