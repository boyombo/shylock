#!/usr/bin/env python
from datewidget import DateTimeWidget
from django import forms
from datetime import date

class MyDateField(forms.DateField):
    widget = DateTimeWidget

    def __init__(self, *args, **kwargs):
        super(MyDateField, self).__init__()
        self.input_formats = ('%Y-%m-%d',)

class DateRangeForm(forms.Form):
    start = MyDateField(initial=date.today)
    end = MyDateField(initial=date.today)

    def clean(self):
        if 'end' in self.cleaned_data and 'start' in self.cleaned_data:
            if self.cleaned_data['end'] < self.cleaned_data['start']:
                raise forms.ValidationError('The start date must be before the end date')
        return self.cleaned_data
