from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest
from .forms import *
from .models import *
# Create your views here.

def enter_view(request: HttpRequest):

    if request.user.is_authenticated:
        return redirect("library")
    
    return redirect("login")

def login_view(request: HttpRequest):

    if request.user.is_authenticated:
        return redirect("library")

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)

                return redirect("library")
            
        return render(request, "main/login.html", { 'form': form, 'error_during_login': True })
                
    else:

        return render(request, "main/login.html", { 'form': LoginForm()})

def logout_view(request: HttpRequest):

    logout(request)

    return redirect("login")


def library_view(request: HttpRequest):

    if not request.user.is_authenticated:
        return redirect("login")

    filters = dict()

    for categories in CardTagsCategoriesModel.objects.all():
        filters[categories.category_name] = list(map(lambda el: (el.tag_name, "{}-{}".format(el.tag_name.lower().replace(' ', '-'), el.id)), CardTagsModel.objects.filter(category_id=categories)))

    if request.method == "GET":
        form = SearchForm(request.GET)

        print(form.errors)

        if form.is_valid():

            return render(request, "main/index.html", { 'filters': filters, 'cards': CardContentModel.objects.filter(card_name__icontains = form.cleaned_data['query']), 'form' : form })

    return render(request, "main/index.html", { 'filters': filters, 'cards': CardContentModel.objects.all(), 'form': SearchForm() })

def upload_view(request: HttpRequest):

    if not request.user.is_authenticated:
        return redirect("login")
    
    if request.method == "POST":
        form = UploadForm(request.POST, request.FILES)

        if form.is_valid():
            newCard = CardContentModel(
                card_name=form.cleaned_data['card_name'],
                card_description=form.cleaned_data['card_description'],
                author=request.user
            )

            newCard.save()

            newCard.blender_mesh = form.cleaned_data['blender_mesh']
            newCard.fbx_mesh = form.cleaned_data['fbx_mesh']
            newCard.preview_mesh = form.cleaned_data['preview_mesh']

            newCard.save()

            return redirect("library")

        return render(request, "main/upload.html", {'form': form})

    return render(request, "main/upload.html", {'form': UploadForm()})


