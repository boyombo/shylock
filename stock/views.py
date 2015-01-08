from django.views.generic.list_detail import object_list
from django.shortcuts import render_to_response, redirect, get_object_or_404
from stock.models import Item, Category, Location, Stock
from stock.forms import ItemForm, CategoryForm, LocationForm
from django.db.models import Q
from django.conf import settings
from django.core import serializers
from django.http import HttpResponse, HttpResponseBadRequest
from django.template import Template
from django.template.context import Context, RequestContext
from django.template.loader import render_to_string
from django.contrib import messages


def stock_locations(request):
    return object_list(
        request,
        queryset=Location.objects.all(),
        allow_empty=True,
        template_name='stock/location_list.html'
    )


def newlocation(request, pk=None):
    if pk:
        location = get_object_or_404(Location, pk=pk)
    else:
        location = None
    if request.method == 'POST':
        form = LocationForm(request.POST, instance=location)
        if form.is_valid():
            location = form.save()
            messages.info(request, 'Your Location has been saved')
            return redirect('stock_locations')
    else:
        form = LocationForm(instance=location)
    return render_to_response('stock/newlocation.html', {'form': form},
                              context_instance=RequestContext(request))


def stock_categories(request):
    return object_list(
        request,
        queryset=Category.objects.all(),
        allow_empty=True,
        template_name='stock/category_list.html'
    )


def newcategory(request, id=None):
    if id:
        category = get_object_or_404(Category, pk=id)
    else:
        category = None
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category = form.save()
            messages.info(request, 'Your category has been saved')
            return redirect('stock_categories')
    else:
        form = CategoryForm(instance=category)
    return render_to_response(
        'stock/newcategory.html', {'form': form},
        context_instance=RequestContext(request))


def stock_list(request):
    loc = request.GET.get('location', '')
    if loc:
        location = Location.objects.get(pk=loc)
        items = [
            (
                stock.item.description,
                stock.quantity,
                stock.item.cost_price,
                stock.item.selling_price
            ) for stock in Stock.objects.filter(location=location)
        ]
    else:
        location = None
        items = [
            (
                item.description,
                item.quantity,
                item.cost_price,
                item.selling_price
            ) for item in Item.objects.all()
        ]
    locations = Location.objects.all()
    return render_to_response(
        'stock/stock_list.html',
        {
            'items': items,
            'locations': locations,
            'current_location': location,
            'current_location_pk': loc,
        },
        context_instance=RequestContext(request))
    return object_list(
            request,
            queryset=Item.objects.all(),
            allow_empty=True,
            template_name='stock/stock_list.html',
        )


def newitem(request, id=None, next='stock_newitem'):
    if id:
        item = get_object_or_404(Item, pk=id)
    else:
        item = None
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            location = form.cleaned_data.pop('location')
            item = form.save()
            qty = form.cleaned_data['quantity']
            Stock.objects.create(location=location, item=item, quantity=qty)
            messages.info(request, 'Your item has been saved')
            return redirect(next)
    else:
        form = ItemForm(instance=item)
    return render_to_response('stock/newitem.html', {'form': form},
                              context_instance=RequestContext(request))


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
