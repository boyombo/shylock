#from django.views.generic.list_detail import object_list
from django.shortcuts import render
#from django.views.generic.list import ListView
from django.apps import apps
from django.conf import settings
from datetime import datetime
from extras.daterange import DateRangeForm


def simple_list(request, app_label, model_name, date_field=None, template_name='simplereports/object_list.html'):
    #import pdb;pdb.set_trace()
    extra_context = {}
    qset = apps.get_model(app_label, model_name)._default_manager.all()
    page = request.GET.get('page','1')
    if date_field:
        end_date = datetime.now()
        start_date = datetime(end_date.year, end_date.month, 1)
        if request.GET.has_key('start'):
            form = DateRangeForm(request.GET)
            if form.is_valid():
                start_date = form.cleaned_data['start']
                end_date = form.cleaned_data['end']
        else:
            form = DateRangeForm(initial={'start': start_date, 'end': end_date})
        qset = qset.filter(**{str(date_field) + '__range': (start_date, end_date)})
        #extra_context should have start and end if datefield is specified
        extra_context.update({'start': start_date, 'end':end_date, 'form': form})
    return render(
        template_name,
        {
            'queryset': qset,
            'paginate_by': settings.ITEMS_PER_PAGE,
            'page': page,
            'start': start_date,
            'end': end_date,
            'form': form
        })
    #return object_list(
    #    request,
    #    queryset=qset,
    #    paginate_by=settings.ITEMS_PER_PAGE,
    #    page=page,
    #    template_name=template_name,
    #    extra_context=extra_context
    #)


# Create your views here.
