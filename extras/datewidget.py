#!/usr/bin/env python

from django import forms
from django.forms import fields, models, widgets

#################
# CUSTOM FIELDS #
#################

class DateTimeWidget(widgets.DateInput):
    """
    A Calendar widget, which uses the jQuery UI Calendar.
    """
    class Media:
        extend = False
        css = {
            'all': ('css/jquery-ui-themeroller.css',)
                }
        js = ('js/jquery.form.js','js/ui.datepicker.js', 'js/calendar-init.js')
        
    def __init__(self, attrs={}):
        attrs['class'] = 'vDateField'
        super(DateTimeWidget, self).__init__(attrs, format='%d/%m/%Y')
