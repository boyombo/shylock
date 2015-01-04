#!/usr/bin/env python
from sale.models import Cart
from django import template

register = template.Library()

@register.inclusion_tag('_cart.html')
def show_cart(cart_id):
    items = Cart.objects.filter(session_key=cart_id)
    return {'items': items}
