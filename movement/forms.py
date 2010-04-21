from django import forms
#from movement.models import Reception, Transfer
from movement.models import Reception, Return
#from stock.models import LocationItems
from extras.datewidget import DateTimeWidget

class ReceptionForm(forms.ModelForm):
    date = forms.DateField(widget=DateTimeWidget(), input_formats=['%d/%m/%Y'])
    class Meta:
        model = Reception

class ReturnForm(forms.ModelForm):
    date = forms.DateField(widget=DateTimeWidget())
    
    class Meta:
        model = Return

#class TransferForm(forms.ModelForm):
#    date = forms.DateField(widget=DateTimeWidget())
#    class Meta:
#        model = Transfer
#
#    def clean(self):
#        if 'item' in self.cleaned_data and 'quantity' in self.cleaned_data and 'from_location' in self.cleaned_data:
#            try:
#                loc_item = LocationItems.objects.get(location=self.cleaned_data['from_location'], item=self.cleaned_data['item'])
#            except LocationItems.DoesNotExist:
#                raise forms.ValidationError('There is zero stock of this item here')
#            else:
#                if loc_item.quantity < self.cleaned_data['quantity']:
#                    raise forms.ValidationError('Not enough of this item to transfer')
#            return self.cleaned_data
