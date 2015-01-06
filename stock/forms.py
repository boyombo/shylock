from django import forms
from stock.models import Item, Category, Location


class LocationForm(forms.ModelForm):

    class Meta:
        model = Location


class CategoryForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}))

    class Meta:
        model = Category


class ItemForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}))

    class Meta:
        model = Item
