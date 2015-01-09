from django import forms
from stock.models import Item, Category, Location
from supplier.models import Supplier


class SupplierForm(forms.ModelForm):

    class Meta:
        model = Supplier


class LocationForm(forms.ModelForm):

    class Meta:
        model = Location


class CategoryForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}))

    class Meta:
        model = Category


class ItemForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}))
    location = forms.ModelChoiceField(queryset=Location.objects.all())
    quantity = forms.IntegerField(required=False)

    class Meta:
        model = Item
