#!/usr/bin/env python
from django import forms
from expenses.models import Expense
from extras.datewidget import DateTimeWidget

class ExpenseForm(forms.ModelForm):
    date = forms.DateTimeField(widget=DateTimeWidget)
    
    class Meta:
        model = Expense
