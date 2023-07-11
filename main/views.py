from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from .forms import *
from content.models import *
from django.db.models import Case, When, Value, IntegerField

@login_required(login_url='/auth/', redirect_field_name=None)
def library_view(request: HttpRequest):

    assets = Asset.objects.none()

    if request.user.has_perm("content.see_own"):
        assets = Asset.objects.filter(author = request.user.pk)

    if request.user.has_perm("content.see_others"):
        assets = Asset.objects.all()

    assets.order_by()

    assets = assets.annotate(order=Case(When(favorites__pk=request.user.pk, then=Value(0)), default=Value(1), output_field=IntegerField(),)).order_by("order")

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

    return render(request, "main/index.html", { 'filters': AssetTagCategory.get_dictionary(), 'assets': assets[:20] })

@login_required(login_url='/auth/', redirect_field_name=None)
def assets_view(request: HttpRequest):

    print(request.POST)

    assets = Asset.objects.none()

    if request.user.has_perm("content.see_own"):
        assets = Asset.objects.filter(author = request.user.pk)

    if request.user.has_perm("content.see_others"):
        assets = Asset.objects.all()

    assets.order_by()

    assets = assets.annotate(order=Case(When(favorites__pk=request.user.pk, then=Value(0)), default=Value(1), output_field=IntegerField(),)).order_by("order")

    if request.method == 'POST':

        if 'query' in request.POST:
            assets = assets.filter(name__icontains = request.POST.get('query'))

        if 'tags[]' in request.POST:
            for tag in request.POST.getlist('tags[]'):
                assets = assets.filter(tags__in = tag)

        return render(request, "main/asset_template.html", { 'filters': AssetTagCategory.get_dictionary(), 'assets': assets[:20] })

    return render(request, "main/asset_template.html", { 'assets': assets[:20] })

