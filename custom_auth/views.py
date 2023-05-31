from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest
from .forms import LoginForm    

def auth_view(request: HttpRequest):

    if request.user.is_authenticated:
        return redirect('library')

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)

                return redirect('library')
            
        return render(request, "custom_auth/login.html", { 'form': form, 'error_during_login': True })
      
    else:

        return render(request, "custom_auth/login.html", { 'form': LoginForm() })
    
def logout_view(request: HttpRequest):

    if request.user.is_authenticated:
        logout(request)

    return redirect('auth')
