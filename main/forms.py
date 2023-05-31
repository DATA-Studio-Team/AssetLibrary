from django import forms

class SearchForm(forms.Form):
    query = forms.CharField(min_length=1, max_length=50, initial="")