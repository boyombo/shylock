from django.views.generic.list_detail import object_list
from expenses.models import Category, Expense
from expenses.forms import ExpenseForm
from extras.daterange import DateRangeForm
from django.conf import settings
from django.shortcuts import render_to_response, redirect
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
from datetime import date, timedelta

def list_categories(request):
    page = request.GET.get('page', '1')
    return object_list(
        request,
        queryset=Category.objects.all(),
        paginate_by=settings.ITEMS_PER_PAGE,
        page=page,
        template_name='expenses/categories.html',
    )
    
def list_expense(request):
    qset = Expense.objects.all()
    if request.GET.has_key('start'):
        form = DateRangeForm(request.GET)
        #import pdb;pdb.set_trace()
        if form.is_valid():
            start_date , end_date = form.cleaned_data['start'], form.cleaned_data['end']
            qset = qset.filter(date__range=(start_date, end_date))
        else:
            qset = qset.none()
    else:
        form = DateRangeForm()
        end_date = date.today()
        start_date = end_date + timedelta(-7)#a week ago by default
    page = request.GET.get('page','1')
    return object_list(
            request,
            queryset=qset,
            paginate_by=settings.ITEMS_PER_PAGE,
            page=page,
            template_name='expenses/list.html',
            extra_context={'form': form, 'start':start_date, 'end':end_date}
            )

def new_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            request.user.message_set.create(message="Expense added!")
            return redirect('expense_new')
    else:
        form = ExpenseForm()
    return render_to_response('expenses/expense.html', {'form':form}, context_instance=RequestContext(request))