from sale.models import Invoice, Sale, Customer
from stock.models import Item
from django import forms

class SaleForm(forms.ModelForm):
    item = forms.ModelChoiceField(queryset=Item.objects.all(), widget=forms.Select(attrs={'class':'formset-item'}))
    price = forms.DecimalField(widget=forms.TextInput(attrs={'class':'very-short', 'readonly':'readonly'}))
    quantity = forms.FloatField(widget=forms.TextInput(attrs={'class':'very-short'}))
    
    class Meta:
        model = Sale
        exclude = ('invoice',)

class InvoiceForm(forms.ModelForm):
    
    class Meta:
        model = Invoice
        exclude = ('teller', 'date', 'customer')

    def clean_customer(self):
        customer, created = Customer.objects.get_or_create(name=self.cleaned_data['name'])
        return customer

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        exclude = ('address','phone')

class SelectItemForm(forms.Form):
    item = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'long'}))
    #session_key = forms.CharField(max_length=10, widget=forms.HiddenInput)
    
    def clean_item(self):
        try:
            item = Item.objects.get(code__iexact=self.cleaned_data['item'])
        except Item.DoesNotExist:
            try:
                item = Item.objects.get(description__iexact=self.cleaned_data['item'])
            except Item.DoesNotExist:
                raise forms.ValidationError("The item does not exist.")
        return item
