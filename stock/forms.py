from django import forms
from django.contrib.auth.models import User
#from django.db import IntegrityError
from stock.models import Item, Category, Location, UserAccount, SerialItem
from supplier.models import Supplier


class SupplierForm(forms.ModelForm):

    class Meta:
        model = Supplier


class LocationForm(forms.ModelForm):

    class Meta:
        model = Location


class UserAccountForm(forms.Form):
    user_name = forms.CharField(max_length=50)
    password1 = forms.CharField(max_length=10, widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=10, widget=forms.PasswordInput)
    readonly = forms.BooleanField(required=False)
    location = forms.ModelChoiceField(queryset=Location.objects.all())

    def clean_password1(self):
        data = self.cleaned_data
        if 'password1' in data and 'password2' in data:
            if data['password1'] != data['password2']:
                raise forms.ValidationError('The two passwords must match!')
        return data['password1']

    def clean_user_name(self):
        if 'user_name' in self.cleaned_data:
            try:
                User.objects.get(username=self.cleaned_data['user_name'])
            except User.DoesNotExist:
                return self.cleaned_data['user_name']
            else:
                raise forms.ValidationError('The username already exists')

    def clean(self):
        data = self.cleaned_data
        if 'password1' in data and 'password2' in data:
            if data['password1'] != data['password2']:
                raise forms.ValidationError('The two passwords must match!')

        if 'user_name' in data and 'password1' in data:
            username = self.cleaned_data['user_name']
            pwd = self.cleaned_data['password1']
            usr = User.objects.create_user(username, '', pwd)
            self.cleaned_data['user_name'] = usr

            return self.cleaned_data


class EditUserForm(forms.ModelForm):

    class Meta:
        model = UserAccount
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        super(EditUserForm, self).__init__(*args, **kwargs)
        user = kwargs['instance'].user
        self.fields['active'] = forms.BooleanField(
            required=False, initial=user.is_active)
        #self.fields['user'] = kwargs['instance'].user


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


class SerialForm(forms.ModelForm):

    class Meta:
        exclude = ('sale_date', 'customer')
        model = SerialItem
