from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, Http404
from django.contrib.auth.decorators import login_required, permission_required
from .models import *
from .forms import *
from django.utils import timezone
from django.db.models import Q

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
    
    return render(request, "content/view.html", { 'asset': asset, 'relatives': list(map(lambda el: el.second, asset.first_asset.all())) + list(map(lambda el: el.first, asset.second_asset.all())) })

@login_required(login_url='/auth/', redirect_field_name=None)
def add_relation_action(request: HttpRequest, asset_pk):

    asset = Asset.objects.filter(pk=asset_pk)

    if not asset.exists():
        return Http404()
    
    asset = asset.first()

    if not request.user.has_perm("content.edit_own") and asset.author == request.user:
        return Http404()
    
    if not request.user.has_perm("content.edit_others") and asset.author != request.user:
        return Http404()
    
    if not 'asset_id' in request.POST:
        return Http404()

    second_asset = Asset.objects.filter(pk=request.POST['asset_id'])

    if not second_asset.exists():
        return Http404()
    
    second_asset = second_asset.first()

    asset_relation = AssetRelation(first=asset, second=second_asset)
    asset_relation.save()

    return redirect('asset_view', asset_pk)

@login_required(login_url='/auth/', redirect_field_name=None)
def delete_action(request: HttpRequest, asset_pk):

    asset = Asset.objects.filter(pk=asset_pk)

    if not asset.exists():
        return redirect('library')
    
    asset = asset.first()
    
    if not request.user.has_perm("content.delete_own") and asset.author == request.user:
        return redirect('library')
    
    if not request.user.has_perm("content.delete_others") and asset.author != request.user:
        return redirect('library')
    
    asset.delete()

    return redirect('library')

@login_required(login_url='/auth/', redirect_field_name=None)
@permission_required(perm="content.upload", login_url='/auth/')
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
def edit_view(request: HttpRequest, asset_pk):

    asset = Asset.objects.filter(pk=asset_pk)

    if not asset.exists():
        return Http404()
    
    asset = asset.first()

    if not request.user.has_perm("content.edit_own") and asset.author == request.user:
        return Http404()
    
    if not request.user.has_perm("content.edit_others") and asset.author != request.user:
        return Http404()
    
    if request.method == 'POST':

        if 'deleteTexture' in request.POST:

            texture = Texture.objects.filter(pk=request.POST['texture_id'])

            if not texture.exists():
                return Http404()

            texture = texture.first()

            asset.textures.remove(texture)

            texture.delete()

            return HttpResponse(status=200)
        
        else:
            form = UploadForm(request.POST, request.FILES)

            if form.is_valid():

                asset.last_update = timezone.now()

                asset.name = form.cleaned_data['card_name']
                asset.description = form.cleaned_data['card_description']

                if form.cleaned_data['blender_mesh'] is not None:
                    asset.blender_mesh = form.cleaned_data['blender_mesh']

                if form.cleaned_data['fbx_mesh'] is not None:
                    asset.fbx_mesh = form.cleaned_data['fbx_mesh']

                if form.cleaned_data['preview_mesh'] is not None:
                    asset.preview_mesh = form.cleaned_data['preview_mesh']

                for textureFile in request.FILES.getlist('textures'):
                    newTexture = Texture()
                    newTexture.save()

                    newTexture.texture = textureFile

                    newTexture.save()

                    asset.textures.add(newTexture)

                asset.tags.clear()

                for tagId in request.POST.getlist('tags[]'):
                    tag = AssetTag.objects.get(pk=tagId)

                    if tag is not None:
                        asset.tags.add(tag)

                asset.save()

    return render(request, "content/edit.html", { 'asset': asset, 'filters': AssetTagCategory.get_dictionary() })

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