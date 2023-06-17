from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from .forms import *
from content.models import *

@login_required(login_url='/auth/')
def library_view(request: HttpRequest):

    assets = Asset.objects.none()

    if request.user.has_perm("content.see_own"):

        assets = Asset.objects.filter(author = request.user.pk)

    if request.user.has_perm("content.see_others"):
        assets = Asset.objects.all()
    

    if request.method == 'GET':
        form = SearchForm(request.GET)

        if form.is_valid():

            return render(request, "main/index.html", { 'filters': AssetTagCategory.get_dictionary(), 'assets': assets.filter(name__icontains = form.cleaned_data['query']), 'form' : form })



    return render(request, "main/index.html", { 'filters': AssetTagCategory.get_dictionary(), 'assets': assets, 'form': SearchForm() })



