from django.forms import ModelForm
from django import forms
from .models import Reseller, Customer
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth import (authenticate, get_user_model, password_validation,)

class ResellerForm(ModelForm):
    class Meta:
        model = Reseller
        exclude = ["user",'reseller_name','reseller_email']

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        exclude = ["user",'customer_name','customer_email']


class registerForm(forms.ModelForm):
    password = forms.CharField(label = 'Password', widget = forms.PasswordInput(),strip=False,help_text=password_validation.password_validators_help_text_html(),)
    password2 = forms.CharField(label = 'Repeat Password', widget = forms.PasswordInput(),strip=False,help_text="Both Passwords should be same.",)
    #email = forms.EmailField(label = 'Email Address', widget = forms.TextInput())
    domain = forms.CharField(label = 'Domain', widget = forms.TextInput())
    logo = forms.ImageField()
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
        ]

    #Cleaning Method for password Match..........
    def clean_password2(self):
        cd = self.cleaned_data
        if self.cleaned_data.get('password') != cd['password2']:
            raise forms.ValidationError("Passwords don't match.")
        return cd['password2']

    #Cleaning Method for Email Unique..........
    #def clean(self):
    #    if self.cleaned_data.get('email') is None:
    #        raise ValidationError("Enter a valid E-mail Address")
    #    varEmail = self.cleaned_data.get('email').lower()
    #    if User.objects.filter(email = varEmail).count() != 0 :
    #        if not User.objects.get(email = varEmail).is_active :
    #            User.objects.get(email = varEmail).delete()
    #        else:
    #            raise ValidationError(self.cleaned_data.get('email') + "\tAlready Exists.")

