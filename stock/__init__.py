#from django.db.models.signals import post_save
#from movement.models import Transfer
#from stock.models import Location, Item, LocationItems
#
#def modify_stock(sender, instance, created, **kwargs):
#    if sender == Transfer and created:
#        from_stk = LocationItems.objects.get(location=instance.from_location, item=instance.item)
#        from_stk.quantity -= instance.quantity
#        from_stk.save()
#        try:
#            to_stk = LocationItems.objects.get(location=instance.to_location, item=instance.item)
#        except LocationItems.DoesNotExist:
#            LocationItems.objects.create(location=instance.to_location, item=instance.item, quantity=instance.quantity)
#        else:
#            to_stk.quantity += instance.quantity
#            to_stk.save()
#
#post_save.connect(modify_stock)
