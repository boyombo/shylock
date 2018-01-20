#from django.shortcuts import render

#from django.views.generic.list_detail import object_list
from django.views.generic.list import ListView
from supplier.models import Supplier
from django.conf import settings


class SupplierListView(ListView):
    model = Supplier


def simple_list(request):
    page = request.GET.get('page', '1')
    return object_list(
        request,
        queryset=Supplier.objects.all(),
        paginate_by=settings.ITEMS_PER_PAGE,
        page=page,
        template_name='supplier/list.html',
        template_object_name='supplier'
    )
