from django.shortcuts import render

from sale.models import Customer, Sale, Cart, Invoice, get_next_invoice
from stock.models import Item
from sale.forms import InvoiceForm, SelectItemForm, CustomerForm
from extras.daterange import DateRangeForm
#from django.views.generic.list_detail import object_list
from django.views.generic.list import ListView
from django.conf import settings
from django.contrib import messages
from django.template.context import RequestContext
from django.template import Template
from django.template.context import Context
from django.template.loader import render_to_string
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.http import Http404, HttpResponse, HttpResponseBadRequest
from django.db.models import Q
from random import random
from datetime import date, timedelta
import json
import logging
import os

LOGFILE = os.path.join(settings.BASE_DIR, 'logfile.log')
FMT = '[%(asctime)s] %(levelname)s %(message)s'
logging.basicConfig(filename=LOGFILE, level=logging.DEBUG, format=FMT)


class CustomerListView(ListView):
    model = Customer


def customer_list(request):
    page = request.GET.get('page','1')
    return object_list(
            request,
            queryset=Customer.objects.all(),
            paginate_by=settings.ITEMS_PER_PAGE,
            page=page,
            template_name='sale/customer_list.html',
            template_object_name='customer'
            )

def sale_list(request):
    qset = Sale.objects.all()
    if request.GET.has_key('start'):
        form = DateRangeForm(request.GET)
        if form.is_valid():
            start_date, end_date = form.cleaned_data['start'], form.cleaned_data['end']
            qset = qset.filter(invoice__date__range=(start_date, end_date))
        else:
            qset = qset.none()
    else:
        form = DateRangeForm()
        end_date = date.today()
        start_date = end_date + timedelta(-7)#a week ago
    page = request.GET.get('page','1')
    return object_list(
            request,
            queryset=qset,
            paginate_by=settings.ITEMS_PER_PAGE,
            page=page,
            template_name='sale/sale_list.html',
            template_object_name='sale',
            extra_context={'form':form}
            #extra_context={'form':form, 'start': start_date, 'end': end_date},
            )

def sale_new(request):
    if request.method == 'POST':
        #import pdb;pdb.set_trace()
        data = dict(request.POST.copy())
        logging.debug('request data: %s' % data)
        invoiceform = InvoiceForm(request.POST)
        if invoiceform.is_valid():
            discount = invoiceform.cleaned_data['discount']
        customerform = CustomerForm(request.POST)
        if customerform.is_valid():
            customer_name = customerform.cleaned_data['name']
            cust, _ = Customer.objects.get_or_create(name__iexact=customer_name)
        else:
            cust = None
        data.pop('name')
        data.pop('discount')
        if not data:
            logging.error('no items in cart')
            return HttpResponseBadRequest('There are no items in the cart')
        #check if any of the keys is not a valid item.
        items = Item.objects.filter(code__in=data.keys())
        if items.count() < len(data):
            logging.error('invalid items')
            return HttpResponseBadRequest('The items sent are invalid.')#how do we get this?
        invoice = Invoice(teller=request.user, discount=discount, customer=cust)
        invoice.save()
        logging.info('saved invoice')
        #import pdb;pdb.set_trace()
        for key, value in data.items():
            Sale.objects.create(
                invoice=invoice,
                item=items.get(code=key),
                quantity=float(value[0]))
        logging.info('sale successful')
        return HttpResponse('The sale is successful')
    else:
        form = InvoiceForm()
        itemform = SelectItemForm()
        customerform = CustomerForm()
    next_invoice = get_next_invoice()
    cntxt = {
        'invoiceform': form,
        'itemform': itemform,
        'customerform': customerform,
        'invoice_number': next_invoice
    }
    return render(request, 'sale/sale.html', cntxt)
    #return render_to_response(
    #        'sale/sale.html',
    #        {
    #            'invoiceform': form,
    #            'itemform': itemform,
    #            'customerform': customerform,
    #            'invoice_number': Invoice.objects.next_number,
    #        },
    #        context_instance=RequestContext(request))


def get_price(request):
    item_id = request.GET.get('item', '')
    item = get_object_or_404(Item, pk=item_id)
    return HttpResponse(u'{}'.format(item.selling_price))


def customer_complete(request):
    qset = Customer.objects.filter(name__icontains=request.GET.get('q', ''))
    result = ''.join(['{}|{}\n'.format(c.name, c.id) for c in qset])
    return HttpResponse(result)


def item_complete(request):
    q = request.GET.get('q', '')
    qset = Item.objects.filter(Q(description__icontains=q) | Q(code__icontains=q))
    result = ''.join([u'{}|{}\n'.format(i.description, i.id) for i in qset])
    return HttpResponse(result)


def add_to_cart(form, ajax=False):
    '''get the details of an item

    the code or name is posted here'''
    #form = SelectItemForm(request.POST)
    if form.is_valid():
        try:
            cart = Cart.objects.get(session_key=form.cleaned_data['session_key'], item=form.cleaned_data['item'])
        except Cart.DoesNotExist:
            cart = Cart(**form.cleaned_data)
            cart.save()
        else:
            cart.qty += 1
            cart.save()
        item_dict = [(item) for item in cart.item]
        return cart.item


def delete_cart(session):
    id = session.pop('cart_id')
    Cart.objects.filter(session_key=id).delete()


def json_api(request):
    data = {'text': 'ok'}
    response = HttpResponse(json.dumps(data), mimetype='text/json')
    return response
