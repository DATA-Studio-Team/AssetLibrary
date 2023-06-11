from django.shortcuts import render, redirect
from django.http import HttpRequest
from .forms import *
from content.models import *

def enter_view(request: HttpRequest):

    if request.user.is_authenticated:
        return redirect('library')
    
    return redirect('auth')

def library_view(request: HttpRequest):

    if not request.user.is_authenticated:
        return redirect('auth')

    if request.method == 'GET':
        form = SearchForm(request.GET)

        print(form.errors)

        if form.is_valid():

            return render(request, "main/index.html", { 'filters': AssetTagCategory.get_dictionary(), 'assets': Asset.objects.filter(name__icontains = form.cleaned_data['query']), 'form' : form })

    return render(request, "main/index.html", { 'filters': AssetTagCategory.get_dictionary(), 'assets': Asset.objects.all(), 'form': SearchForm() })



