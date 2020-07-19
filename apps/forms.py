from django import forms

from .models import User

class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'gender', 'country', 'ethnicity', 'age']

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
