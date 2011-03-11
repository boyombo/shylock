from django.db.models.signals import post_save
from sale.models import CostOfSale, Sale
from decimal import Decimal

def post_sale_updates(sender, **kwargs):
    sale = kwargs['instance']
    cost_of_sale = CostOfSale(sale=sale, amount=sale.item.cost_price* Decimal(str(sale.quantity)))
    cost_of_sale.save()

post_save.connect(post_sale_updates, sender=Sale)
