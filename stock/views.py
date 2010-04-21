from django.views.generic.list_detail import object_list
#from django.template.context import RequestContext
#from django.shortcuts import render_to_response, redirect, get_object_or_404
from stock.models import Item
from django.db.models import Q
from django.conf import settings
from django.core import serializers
from django.http import HttpResponse, HttpResponseBadRequest
from django.template import Template
from django.template.context import Context
from django.template.loader import render_to_string

def stock_list(request):
    page = request.GET.get('page', '1')
    return object_list(
            request,
            queryset=Item.objects.all(),
            paginate_by=settings.ITEMS_PER_PAGE,
            page=page,
            template_name='stock/stock_list.html',
            template_object_name='stock'
            )

def get_item(request):
    code = request.GET.get('code')
    #import pdb;pdb.set_trace()
    item = Item.objects.filter(Q(code__iexact=code)|Q(description__iexact=code))
    #serialize to json
    if not item:
        return HttpResponseBadRequest('Invalid item code or description')
    json = serializers.serialize('json', item)
    return HttpResponse(json)

def get_row(request):
    code = request.GET.get('code')
    item = Item.objects.get(code=code)
    row = render_to_string('_cart_item.html', {'item': item, 'MEDIA_URL': settings.MEDIA_URL})
    return HttpResponse(row)