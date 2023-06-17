from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required, permission_required
from .models import *
from .forms import *

@login_required(login_url='/auth/')
@permission_required(perm="content.upload_assets", login_url='/auth/')
def upload_view(request: HttpRequest):
    
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)

        if form.is_valid():
            newCard = Asset(
                name=form.cleaned_data['card_name'],
                description=form.cleaned_data['card_description'],
                author=request.user
            )

            newCard.save()

            newCard.blender_mesh = form.cleaned_data['blender_mesh']
            newCard.fbx_mesh = form.cleaned_data['fbx_mesh']
            newCard.preview_mesh = form.cleaned_data['preview_mesh']

            for textureFile in request.FILES.getlist('textures'):
                newTexture = Texture()
                newTexture.save()

                newTexture.texture = textureFile

                newTexture.save()

                newCard.textures.add(newTexture)

            for tagId in request.POST.getlist('tags[]'):
                tag = AssetTag.objects.get(pk=tagId)

                if tag is not None:
                    newCard.tags.add(tag)

            newCard.save()

            return redirect('library')

        return render(request, "content/upload.html", { 'form': form, 'filters': AssetTagCategory.get_dictionary() })

    return render(request, "content/upload.html", { 'form': UploadForm(), 'filters': AssetTagCategory.get_dictionary() })
