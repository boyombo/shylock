from datetime import datetime

from movement.models import Reception, Return, Transfer
from movement.forms import ReceptionForm, ReturnForm, TransferForm
from stock.views import not_readonly

from django.conf import settings
from django.shortcuts import render, redirect
#from django.template.context import RequestContext
#from django.views.generic.list_detail import object_list
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test


def is_superuser(user):
    return user.is_superuser


class ReceptionList(ListView):
    queryset = Reception.objects.all()
    template_name = 'movement/reception_list.html'
    template_object_name = 'reception'


class TransferList(ListView):
    queryset = Transfer.objects.all()
    template_name = 'movement/transfer_list.html'
#def reception_list(request):
#    page = request.GET.get('page', '1')
#    return object_list(
#        request,
#        queryset=Reception.objects.all(),
#        paginate_by=settings.ITEMS_PER_PAGE,
#        page=page,
#        template_name='movement/reception_list.html',
#        template_object_name='reception',
#    )


#def transfer_list(request):
#    return object_list(
#        request,
#        queryset=Transfer.objects.all(),
#        allow_empty=True,
#        template_name='movement/transfer_list.html'
#    )


@user_passes_test(not_readonly)
def transfer_items(request):
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            transfer = form.save(commit=False)
            transfer.when = datetime.now()
            transfer.user = request.user
            transfer.save()
            messages.info(request, 'Transfer is successful')
            return redirect('movement_transfer')
    else:
        form = TransferForm()
    return render(request, 'movement/transfer.html', {'form': form})


@user_passes_test(is_superuser)
def receive(request):
    if request.method == 'POST':
        form = ReceptionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, 'Reception is successful')
            return redirect('movement_receive')
    else:
        form = ReceptionForm()
        #import pdb;pdb.set_trace()
    return render(request, 'movement/receive.html', {'form': form})


#def return_list(request):
#    page = request.GET.get('page', '1')
#    return object_list(
#            request,
#            queryset=Return.objects.all(),
#            #paginate_by=settings.ITEMS_PER_PAGE,
#            #page=page,
#            template_name='movement/return_list.html',
#            #template_object_name='transfer'
#            )

@login_required
@user_passes_test(is_superuser)
def return_items(request):
    if request.method == 'POST':
        form = ReturnForm(request.POST)
        if form.is_valid():
            transfer = form.save(commit=False)
            transfer.user = request.user
            transfer.save()
            messages.info(request, 'The return is successful')
            return redirect('movement_return')
    else:
        form = ReturnForm()
    return render(request, 'movement/return.html', {'form': form})
