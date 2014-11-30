from decimal import Decimal
from YAASApp.models import Bid

__author__ = 'Duong Duc Anh'

from django import forms
from django.contrib.auth.models import User

class CreateUserForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput())
    password_confirm = forms.CharField(max_length=100, widget=forms.PasswordInput())
    email = forms.EmailField(required=False)


    def clean_username(self):
        try:
            User.objects.get(username=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError("this user exist already")


    def clean(self):
        if 'password' in self.cleaned_data and 'password_confirm' in self.cleaned_data:
            if self.cleaned_data['password'] != self.cleaned_data['password_confirm']:
                raise forms.ValidationError("passwords are not matched")
        return self.cleaned_data


    def save(self):
        new_user = User.objects.create_user(username=self.cleaned_data['username'],
                                        password=self.cleaned_data['password'],
                                        email=self.cleaned_data['email'],
    )
        return new_user


class ChangeEmail(forms.Form):
    email = forms.EmailField(label=u'Type new Email',required=False)
    email_confirm = forms.EmailField(label=u'Type Email again',required=False)

class createAuction(forms.Form):
    title = forms.Field(required=True)
    description = forms.CharField(widget=forms.Textarea(), required=True)
    min_price = forms.DecimalField(max_digits=10 ,decimal_places=2)
    end_time = forms.Field(required=True)

class BidForm(forms.Form):
    bid_price = forms.DecimalField(max_digits=10 ,decimal_places=2)
