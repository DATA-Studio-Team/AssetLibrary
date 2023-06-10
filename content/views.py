from django.shortcuts import render, redirect
from django.http import HttpRequest
from .models import *
from .forms import *

def upload_view(request: HttpRequest):

    if not request.user.is_authenticated:
        return redirect('auth')
    
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)

        if form.is_valid():
            newCard = Asset(
                card_name=form.cleaned_data['card_name'],
                card_description=form.cleaned_data['card_description'],
                author=request.user
            )

            newCard.save()

            newCard.blender_mesh = form.cleaned_data['blender_mesh']
            newCard.fbx_mesh = form.cleaned_data['fbx_mesh']
            newCard.preview_mesh = form.cleaned_data['preview_mesh']

            newCard.save()

            return redirect('library')

        return render(request, "content/upload.html", { 'form': form, 'filters': AssetTagCategory.get_dictionary() })

    return render(request, "content/upload.html", { 'form': UploadForm(), 'filters': AssetTagCategory.get_dictionary() })
