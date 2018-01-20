#from django.views.generic.list_detail import object_list
from django.views.generic.list import ListView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.db.models.aggregates import Sum
from django.conf import settings
from django.core import serializers
from django.http import HttpResponse, HttpResponseBadRequest
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test

from supplier.models import Supplier
from stock.models import Item, Category, Location, Stock, UserAccount,\
    SerialItem
from stock.forms import ItemForm, CategoryForm, LocationForm,\
    SupplierForm, UserAccountForm, EditUserForm, SerialForm


class IsSuperMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


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


class StockLocView(ListView):
    queryset = Location.objects.all()
    template_name = 'stock/location_list.html'
#def stock_locations(request):
#    qset = Location.objects.all()
#    return render(request, 'stock/location_list.html', {'qset': qset})
    #return object_list(
    #    request,
    #    queryset=Location.objects.all(),
    #    allow_empty=True,
    #    template_name='stock/location_list.html'
    #)


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
    return render(request, 'stock/newlocation.html', {'form': form})


class StockUsersList(IsSuperMixin, ListView):
    queryset = UserAccount.objects.all()
    template_name = 'stock/user_list.html'
    context_object_name = 'users_list'


#@user_passes_test(is_superuser)
#def stock_users(request):
#    qset = UserAccount.objects.all(),
#    return render(request, 'stock/user_list.html', {'qset': qset})
    #return object_list(
    #    request,
    #    queryset=UserAccount.objects.all(),
    #    allow_empty=True,
    #    template_name='stock/user_list.html'
    #)


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
    return render(request, 'stock/newuser.html', {'form': form})


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
    return render(request, 'stock/edit_user.html', {'form': form, 'usr': usr})


class StockSupplierList(ListView):
    queryset = Supplier.objects.all()
    template_name = 'stock/supplier_list.html'


#def stock_suppliers(request):


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
    return render(request, 'stock/newsupplier.html', {'form': form})


class SerialCategoriesList(IsSuperMixin, ListView):
    queryset = Category.objects.all()
    template_name = 'stock/serial_category_list.html'


class StockCategoriesList(IsSuperMixin, ListView):
    queryset = Category.objects.all()
    template_name = 'stock/category_list.html'


#@user_passes_test(is_superuser)
#def stock_categories(request, template_name='stock/category_list.html'):
#    qset = Category.objects.all()
#    return render(request, template_name, {'qset': qset})


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
    return render(request, template_name, {'form': form})


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
    cntxt = {
        'items': items,
        'locations': locations,
        'current_location': location,
        'current_location_pk': loc,
    }
    return render(request, 'stock/stock_list.html', cntxt)
    #return object_list(
    #    request,
    #    queryset=Item.objects.all(),
    #    allow_empty=True,
    #    template_name='stock/stock_list.html',
    #)


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
    cntxt = {
        'items': SerialItem.objects.all(),
        'instock_count': instock_count,
        'sold_count': sold_count,
        'instock_cost': instock_cost,
        'sold_cost': sold_cost,
        'instock_selling': instock_selling,
        'sold_selling': sold_selling,
    }
    return render(request, 'stock/serial_list.html', cntxt)


def newserial(request, id=None, next='serial_newitem'):
    if request.method == 'POST':
        form = SerialForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(next)
    else:
        form = SerialForm()
    return render(request, 'stock/newserial.html', {'form': form})


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
    return render(request, 'stock/newitem.html', {'form': form})


def get_item(request):
    code = request.GET.get('code')
    #import pdb;pdb.set_trace()
    item = Item.objects.filter(Q(code__iexact=code) | Q(description__iexact=code))
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
