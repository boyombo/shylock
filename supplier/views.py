from django.views.generic.list_detail import object_list
from supplier.models import Supplier
from django.conf import settings

def list(request):
    page = request.GET.get('page','1')
    return object_list(
            request,
            queryset=Supplier.objects.all(),
            paginate_by=settings.ITEMS_PER_PAGE,
            page=page,
            template_name='supplier/list.html',
            template_object_name='supplier'
            )
