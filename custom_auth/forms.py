from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(min_length=3, max_length=30, initial="")
    password = forms.CharField(min_length=4, max_length=100, initial="")
