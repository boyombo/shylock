from movement.models import Reception, Return
from movement.forms import ReceptionForm, ReturnForm
from stock.models import Item
from django.conf import settings
from django.shortcuts import render_to_response, redirect
from django.template.context import RequestContext
from django.views.generic.list_detail import object_list
from django.contrib.auth.decorators import login_required

def reception_list(request):
    page = request.GET.get('page', '1')
    return object_list(
            request,
            queryset=Reception.objects.all(),
            paginate_by=settings.ITEMS_PER_PAGE,
            page=page,
            template_name='movement/reception_list.html',
            template_object_name='reception',
            )

def receive(request):
    if request.method == 'POST':
        form = ReceptionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('movement_reception_list')
    else:
        form = ReceptionForm()
    return render_to_response('movement/receive.html', {'form':form}, context_instance=RequestContext(request))

def return_list(request):
    page = request.GET.get('page', '1')
    return object_list(
            request,
            queryset=Return.objects.all(),
            paginate_by=settings.ITEMS_PER_PAGE,
            page=page,
            template_name='movement/transfer_list.html',
            template_object_name='transfer'
            )

@login_required
def return_items(request):
    if request.method == 'POST':
        form = ReturnForm(request.POST)
        if form.is_valid():
            transfer = form.save(commit=False)
            transfer.user = request.user
            transfer.save()
            return redirect('movement_return_list')
    else:
        form = ReturnForm()
    return render_to_response('movement/transfer.html',
            {'form':form},
            context_instance=RequestContext(request))
