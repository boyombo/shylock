from django.views.generic.list_detail import object_list
from django.db.models import get_model
from django.conf import settings
from django import template
from django.template.loader import get_template
from datetime import datetime, timedelta
from extras.daterange import DateRangeForm

def simple_list(request, app_label, model_name, date_field=None, template_name='simplereports/object_list.html'):
    extra_context = {}
    qset = get_model(app_label, model_name).objects.all()
    page = request.GET.get('page','1')
    if date_field:
        end_date = datetime.now()
        start_date = end_date - timedelta(7)
        if request.GET.has_key('start'):
            form = DateRangeForm(request.GET)
            if form.is_valid():
                start_date, end_date = form.cleaned_data['start'], form.cleaned_data['end']
        else:
            form = DateRangeForm()
        qset = qset.filter(**{str(date_field) + '__range': (start_date, end_date)})
        #extra_context should have start and end if datefield is specified
        extra_context.update({'start': start_date, 'end':end_date, 'form': form})
    return object_list(
        request,
        queryset=qset,
        paginate_by=settings.ITEMS_PER_PAGE,
        page=page,
        template_name=template_name,
        extra_context=extra_context
    )
    