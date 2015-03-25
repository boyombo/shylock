from django.views.generic.list_detail import object_list
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.db.models import Q
from django.db.models.aggregates import Sum
from django.conf import settings
from django.core import serializers
from django.http import HttpResponse, HttpResponseBadRequest
from django.template.context import RequestContext
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test

from supplier.models import Supplier
from stock.models import Item, Category, Location, Stock, UserAccount,\
    SerialItem
from stock.forms import ItemForm, CategoryForm, LocationForm,\
    SupplierForm, UserAccountForm, EditUserForm, SerialForm


def is_superuser(user):
    return user.is_superuser


def not_readonly(user):
    if user.is_superuser:
        return True
    accts = user.useraccount_set.all()
    if not accts:
        # Not created here
        return False
    acct = accts[0]
    if not acct.read_only:
        return True
    return False


def stock_locations(request):
    return object_list(
        request,
        queryset=Location.objects.all(),
        allow_empty=True,
        template_name='stock/location_list.html'
    )


@user_passes_test(is_superuser)
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


@user_passes_test(is_superuser)
def stock_users(request):
    return object_list(
        request,
        queryset=UserAccount.objects.all(),
        allow_empty=True,
        template_name='stock/user_list.html'
    )


@user_passes_test(is_superuser)
def newuser(request):
    if request.method == 'POST':
        form = UserAccountForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user_name']
            readonly = form.cleaned_data['readonly']
            location = form.cleaned_data['location']
            UserAccount.objects.create(
                user=user, location=location, read_only=readonly)
            messages.info(request, 'Account %s has been saved' % user.username)
            return redirect('user_list')
    else:
        form = UserAccountForm()
    return render_to_response('stock/newuser.html', {'form': form},
                              context_instance=RequestContext(request))


@user_passes_test(is_superuser)
def edituser(request, pk):
    usr = get_object_or_404(UserAccount, pk=pk)
    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=usr)
        if form.is_valid():
            usr.user.is_active = form.cleaned_data['active']
            usr.user.save()
            form.save()
            return redirect('user_list')
    else:
        form = EditUserForm(instance=usr)
    return render_to_response(
        'stock/edit_user.html',
        {'form': form, 'usr': usr},
        context_instance=RequestContext(request))


def stock_suppliers(request):
    return object_list(
        request,
        queryset=Supplier.objects.all(),
        allow_empty=True,
        template_name='stock/supplier_list.html'
    )


@user_passes_test(is_superuser)
def newsupplier(request, id=None):
    if id:
        supplier = get_object_or_404(Supplier, pk=id)
    else:
        supplier = None
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            supplier = form.save()
            messages.info(request, 'Your supplier has been saved')
            return redirect('stock_suppliers')
    else:
        form = SupplierForm(instance=supplier)
    return render_to_response(
        'stock/newsupplier.html', {'form': form},
        context_instance=RequestContext(request))


@user_passes_test(is_superuser)
def stock_categories(request, template_name='stock/category_list.html'):
    return object_list(
        request,
        queryset=Category.objects.all(),
        allow_empty=True,
        template_name=template_name
    )


@user_passes_test(is_superuser)
def newcategory(request, id=None, next='stock_categories',
                template_name='stock/newcategory.html'):
    if id:
        category = get_object_or_404(Category, pk=id)
    else:
        category = None
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category = form.save()
            messages.info(request, 'Your category has been saved')
            return redirect(next)
    else:
        form = CategoryForm(instance=category)
    return render_to_response(
        template_name, {'form': form},
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


def serial_list(request):
    serials = SerialItem.objects.all()
    instock_count = serials.filter(sale_date__isnull=True).count() or 0
    sold_count = serials.filter(sale_date__isnull=False).count() or 0
    instock_cost = serials.filter(sale_date__isnull=True).aggregate(
        Sum('cost_price'))['cost_price__sum'] or 0
    sold_cost = serials.filter(sale_date__isnull=False).aggregate(
        Sum('cost_price'))['cost_price__sum'] or 0
    instock_selling = serials.filter(sale_date__isnull=True).aggregate(
        Sum('selling_price'))['selling_price__sum'] or 0
    sold_selling = serials.filter(sale_date__isnull=False).aggregate(
        Sum('selling_price'))['selling_price__sum'] or 0
    return render_to_response(
        'stock/serial_list.html',
        {
            'items': SerialItem.objects.all(),
            'instock_count': instock_count,
            'sold_count': sold_count,
            'instock_cost': instock_cost,
            'sold_cost': sold_cost,
            'instock_selling': instock_selling,
            'sold_selling': sold_selling,
        },
        context_instance=RequestContext(request))


def newserial(request, id=None, next='serial_newitem'):
    if request.method == 'POST':
        form = SerialForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(next)
    else:
        form = SerialForm()
    return render_to_response(
        'stock/newserial.html',
        {'form': form},
        context_instance=RequestContext(request))


@user_passes_test(is_superuser)
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
