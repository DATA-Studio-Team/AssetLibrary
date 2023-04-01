from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpRequest
from .forms import *
# Create your views here.

def login_view(request: HttpRequest):

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)

                return redirect("/index")
            
        return render(request, "main/login.html", { 'form': form, 'error_during_login': True })
                
    else:

        return render(request, "main/login.html", { 'form': LoginForm()})

    

def index_view(request: HttpRequest):

    return render(request, "main/index.html")