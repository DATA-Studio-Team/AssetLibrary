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

    filters = dict()

    for categories in AssetTagCategory.objects.all():
        filters[categories.name] = list(map(lambda el: (el.name, "{}-{}".format(el.name.lower().replace(' ', '-'), el.id)), AssetTag.objects.filter(category_id=categories)))

    if request.method == 'GET':
        form = SearchForm(request.GET)

        print(form.errors)

        if form.is_valid():

            return render(request, "main/index.html", { 'filters': filters, 'cards': Asset.objects.filter(card_name__icontains = form.cleaned_data['query']), 'form' : form })

    return render(request, "main/index.html", { 'filters': filters, 'cards': Asset.objects.all(), 'form': SearchForm() })



