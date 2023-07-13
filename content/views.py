from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, Http404
from django.contrib.auth.decorators import login_required, permission_required
from .models import *
from .forms import *

import os
import zipfile
import io

@login_required(login_url='/auth/', redirect_field_name=None)
def view_view(request: HttpRequest, asset_pk):

    asset = Asset.objects.filter(pk=asset_pk)

    if not asset.exists():
        return redirect('library')
    
    asset = asset.first()
    
    if not request.user.has_perm("content.see_own") and asset.author == request.user:
        return redirect('library')
    
    if not request.user.has_perm("content.see_others") and asset.author != request.user:
        return redirect('library')

    return render(request, "content/view.html", { 'asset': asset })

@login_required(login_url='/auth/', redirect_field_name=None)
def delete_view(request: HttpRequest, asset_pk):

    asset = Asset.objects.filter(pk=asset_pk)

    if not asset.exists():
        return redirect('library')
    
    asset = asset.first()
    
    if not request.user.has_perm("content.edit_own") and asset.author == request.user:
        return redirect('library')
    
    if not request.user.has_perm("content.edit_others") and asset.author != request.user:
        return redirect('library')
    
    asset.delete()

    return redirect('library')

@login_required(login_url='/auth/', redirect_field_name=None)
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

@login_required(login_url='/auth/', redirect_field_name=None)
def download_asset_zip(request: HttpRequest, asset_pk):

    asset = Asset.objects.filter(pk=asset_pk)

    if not asset.exists():
        return Http404()
    
    asset = asset.first()

    if not request.user.has_perm("content.see_own") and asset.author == request.user:
        return Http404()
    
    if not request.user.has_perm("content.see_others") and asset.author != request.user:
        return Http404()
    
    zip_filename = "{}_asset.zip".format(asset.name)

    bytes = io.BytesIO()

    zipFile = zipfile.ZipFile(bytes, "w")

    for file in (asset.blender_mesh.path, asset.fbx_mesh.path):
        fdir, fname = os.path.split(file)
        zipFile.write(file, fname)

    for texture in map(lambda el: el.texture.path, asset.textures.all()):
        fdir, fname = os.path.split(texture)
        fname = os.path.join("textures", fname)
        zipFile.write(texture, fname)

    zipFile.close()

    return HttpResponse(bytes.getvalue(), content_type = "application/x-zip-compressed", headers = { 'Content-Disposition': 'attachment; filename={}'.format(zip_filename) })

@login_required(login_url='/auth/', redirect_field_name=None)
def download_textures_zip(request: HttpRequest, asset_pk):

    asset = Asset.objects.filter(pk=asset_pk)

    if not asset.exists():
        return Http404()
    
    asset = asset.first()

    if not request.user.has_perm("content.see_own") and asset.author == request.user:
        return Http404()
    
    if not request.user.has_perm("content.see_others") and asset.author != request.user:
        return Http404()

    zip_filename = "{}_textures.zip".format(asset.name)

    bytes = io.BytesIO()

    zipFile = zipfile.ZipFile(bytes, "w")

    for texture in map(lambda el: el.texture.path, asset.textures.all()):
        fdir, fname = os.path.split(texture)
        zipFile.write(texture, fname)

    zipFile.close()

    return HttpResponse(bytes.getvalue(), content_type = "application/x-zip-compressed", headers = { 'Content-Disposition': 'attachment; filename={}'.format(zip_filename) })