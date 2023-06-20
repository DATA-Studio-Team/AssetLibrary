from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from .forms import *
from content.models import *
from django.db.models import Case, When, Value, IntegerField

@login_required(login_url='/auth/')
def library_view(request: HttpRequest):

    assets = Asset.objects.none()

    if request.user.has_perm("content.see_own"):
        assets = Asset.objects.filter(author = request.user.pk)

    if request.user.has_perm("content.see_others"):
        assets = Asset.objects.all()
    
    assets.order_by()

    assets = assets.annotate(order=Case(When(favorites__pk=request.user.pk, then=Value(0)), default=Value(1), output_field=IntegerField(),)).order_by("order")

    if request.method == 'GET':
        form = SearchForm(request.GET)

        if form.is_valid():

            return render(request, "main/index.html", { 'filters': AssetTagCategory.get_dictionary(), 'assets': assets.filter(name__icontains = form.cleaned_data['query']), 'form' : form })

    if request.method == 'POST':

        if 'setAsFavourite' in request.POST:
            asset = assets.filter(pk = request.POST['id'])

            if asset.exists():
                asset = asset.first()

                if request.POST['setAsFavourite'] == 'true' and not asset.favorites.contains(request.user):
                    asset.favorites.add(request.user)
                elif request.POST['setAsFavourite'] == 'false' and asset.favorites.contains(request.user):
                    asset.favorites.remove(request.user)

                asset.save()

                return HttpResponse(status=200)
            
            return HttpResponse(status=400)
        
        return HttpResponse(status=404)



    return render(request, "main/index.html", { 'filters': AssetTagCategory.get_dictionary(), 'assets': assets, 'form': SearchForm() })



