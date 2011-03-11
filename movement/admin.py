from django.contrib import admin
from movement.models import Reception, Return

class ReceptionAdmin(admin.ModelAdmin):
    list_display = ('item', 'unit_cost', 'supplier', 'date')
    
admin.site.register(Reception, ReceptionAdmin)
admin.site.register(Return)
