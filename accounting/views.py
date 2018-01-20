from sale.models import Sale, CostOfSale
from expenses.models import Expense, Category
from django.shortcuts import render
from django.db.models.aggregates import Sum, Max
from django.conf import settings
from extras.daterange import DateRangeForm
from datetime import date, timedelta
from decimal import Decimal
from collections import defaultdict
import os


def get_default_dates():
    end_date = date.today()
    start_date = end_date - timedelta(7)
    return start_date, end_date


def pandl(request):
    start = request.GET.get('start', None)
    if start:
        form = DateRangeForm(request.GET)
        if form.is_valid():
            start_date = form.cleaned_data['start']
            end_date = form.cleaned_data['end']
    else:
        form = DateRangeForm()
        start_date, end_date = get_default_dates()
    _sales = sum(sale.price*Decimal(str(sale.quantity)) for sale in Sale.objects.filter(invoice__date__range=(start_date,end_date)))
    _cost_of_sales = CostOfSale.objects.filter(sale__invoice__date__range=(start_date, end_date)).aggregate(Sum('amount'))['amount__sum']
    _expenses = Expense.objects.filter(date__range=(start_date, end_date)).aggregate(Sum('amount'))['amount__sum']
    sales = _sales if _sales else Decimal('0')
    cost_of_sales = _cost_of_sales if _cost_of_sales else Decimal('0')
    expenses = _expenses if _expenses else Decimal('0')
    pl = {
        'sales': sales,
        'cost_of_sales': cost_of_sales,
        'expenses': expenses,
        'gross': sales-cost_of_sales,
        'net': sales-cost_of_sales-expenses,
        }
    if sales:
        pl.update(
            {
                'cos_percent': cost_of_sales*100/sales,
                'gross_percent': (sales - cost_of_sales)*100/sales,
                'net_percent': (sales - cost_of_sales - expenses)*100/sales,
            }
            )
    cntxt = {
        'form': form,
        'pl': pl,
        'start': start_date,
        'end': end_date,
    }
    return render(request, 'accounting/pandl.html', cntxt)


def graph(request):
    """show the sales, cos, exp, profits on a date graph
    """
    start_date, end_date = get_default_dates()
    _start = request.GET.get('start', None)
    if _start:
        form = DateRangeForm(request.GET)
        if form.is_valid():
            start_date = form.cleaned_data['start']
            end_date = form.cleaned_data['end']
    else:
        form = DateRangeForm()
    dates, sales, expenses = get_summaries_by_date(start_date, end_date)
    #data = zip(dates, sales, expenses)
    sales_data = get_series(sales, dates, 'sales')
    expense_data = get_series(expenses, dates, 'expenses')
    #import pdb;pdb.set_trace()
    data = plot_jslinegraph(dates, sales, expenses)
    #plot_linegraph(dates, sales, expenses)
    cntxt = {
        'start': start_date,
        'end': end_date,
        'form': form,
        'dates': dates,
        'sales': sales,
        'sales_data': sales_data,
        'expense_data': expense_data,
        'expenses': expenses,
        'total_sales': sum(sales),
        'total_expenses': sum(expenses),
        'data': data,
    }
    return render(request, 'accounting/graph.html', cntxt)


def get_summaries_by_date(start_date, end_date):
    dates = map(lambda x: start_date + timedelta(x), range((end_date - start_date).days + 1))
    d_sales = defaultdict(Decimal)
    d_expenses = defaultdict(Decimal)
    sales = Sale.objects.filter(invoice__date__range=(start_date, end_date))
    expenses = Expense.objects.filter(date__range=(start_date, end_date))
    for date in dates:
        d_sales[date] += sum(sale.price * Decimal(str(sale.quantity)) for sale in sales.filter(invoice__date=date))
        d_expenses[date] += sum(expense.amount for expense in expenses.filter(date=date))
    sales_values = map(lambda x:d_sales.get(x), dates)
    expense_values = map(lambda x: d_expenses.get(x), dates)
    return dates, sales_values, expense_values


def plot_linegraph(dates, sales, expenses):
    from pylab import plot, hold, xticks, grid, legend, title, savefig, close, arange
    date_label = map(lambda x: x.strftime('%b %d'), dates)
    plot(sales, 'g')
    #hold(True)
    plot(expenses, 'r')
    xticks(arange(len(date_label)), date_label)
    grid()
    legend(['sales', 'expenses'])
    title('Sales and Expense trends')
    filename = os.path.join(settings.MEDIA_ROOT, 'graphs', 'line.png')
    #import pdb;pdb.set_trace()
    savefig(filename)
    close()


def get_series(x, y, label='sales'):
    data = map(lambda (x, y): [y.day, int(x)], zip(x, y))
    return '{label: "%s", data: %s}' % (label, data)


def plot_jslinegraph(dates, sales, expenses):
    def get_series(x, y):
        return map(lambda (x, y): [y.strftime('%b %d'), int(x)], zip(x, y))
    sales_data = {
        'label': 'sales',
        'data': get_series(sales, dates)
    }
    expense_data = {
        'label': 'expenses',
        'data': get_series(expenses, dates)
    }
    return str(map(lambda (x,y,z): [[int(y),int(z)],{'label':x.strftime('%b %d')}], zip(dates, sales, expenses)))
