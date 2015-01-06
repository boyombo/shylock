from django import forms
#from movement.models import Reception, Transfer
from movement.models import Reception, Return, Transfer
from stock.models import Stock
from extras.datewidget import DateTimeWidget
from datetime import date


class ReceptionForm(forms.ModelForm):
    date = forms.DateField(
        widget=DateTimeWidget, initial=date.today, input_formats=['%d/%m/%Y'])

    class Meta:
        model = Reception


class ReturnForm(forms.ModelForm):
    date = forms.DateField(
        widget=DateTimeWidget, initial=date.today, input_formats=['%d/%m/%Y'])

    class Meta:
        model = Return


class TransferForm(forms.ModelForm):
    when = forms.DateField(required=False, widget=DateTimeWidget())

    class Meta:
        model = Transfer

    def clean(self):
        data = self.cleaned_data
        if ('item' in data and 'quantity' in data
                and 'source' in data and 'destination' in data):
            source = self.cleaned_data['source']
            dest = self.cleaned_data['destination']
            item = self.cleaned_data['item']
            qty = self.cleaned_data['quantity']
            try:
                source_stock = Stock.objects.get(location=source, item=item)
            except Stock.DoesNotExist:
                raise forms.ValidationError('No stock to transfer')

            # Check quantity
            if source_stock.quantity < qty:
                raise forms.ValidationError(
                    'Not enough stock. There are only %s left' %
                    source_stock.quantity)

            try:
                dest_stock = Stock.objects.get(location=dest, item=item)
            except Stock.DoesNotExist:
                dest_stock = Stock.objects.create(
                    location=dest, item=item, quantity=qty)

            source_stock.quantity -= qty
            dest_stock.quantity += qty
            source_stock.save()
            dest_stock.save()

            return self.cleaned_data


#            try:
#                loc_item = LocationItems.objects.get(location=self.cleaned_data['from_location'], item=self.cleaned_data['item'])
#            except LocationItems.DoesNotExist:
#                raise forms.ValidationError('There is zero stock of this item here')
#            else:
#                if loc_item.quantity < self.cleaned_data['quantity']:
#                    raise forms.ValidationError('Not enough of this item to transfer')
#            return self.cleaned_data
