from typing import Any, Dict, Tuple
from django.db import models
from django.contrib.auth.models import User

import os

from assetlib import settings

from datetime import datetime

class AssetTagCategory(models.Model):

    class Meta:
        verbose_name = "Asset Category"
        verbose_name_plural = "Asset Categories"

    name = models.CharField(max_length=50)
    order = models.SmallIntegerField(unique=True)

    @staticmethod
    def get_dictionary():
        filters = dict()

        for categories in AssetTagCategory.objects.all():
            filters[categories.name] = list(map(lambda el: (el.name, el.get_named_list(), el.pk), AssetTag.objects.filter(category_id=categories)))

        return filters

    def __str__(self):
        return self.name

class AssetTag(models.Model):

    class Meta:
        verbose_name = "Asset Tag"
        verbose_name_plural = "Asset Tags"

    name = models.CharField(max_length=50)
    category = models.ForeignKey(AssetTagCategory, on_delete=models.CASCADE)

    def get_named_list(self): 
        return "{}-{}".format(self.name.lower().replace(' ', '-'), self.pk)

    def __str__(self):
        return self.name

class Texture(models.Model):

    class Meta:
        verbose_name = "Texture"
        verbose_name_plural = "Textures"

    def content_path(instance, filename):
        return 'textures/{0}/{1}'.format(instance.id, filename)
    
    texture = models.FileField(upload_to=content_path)

    def delete(self, *args, **kwargs):
        self.texture.delete()

        os.rmdir(os.path.abspath(os.path.join(settings.MEDIA_ROOT, 'textures', str(self.pk))))

        return super().delete(args, kwargs)

class Asset(models.Model):

    class Meta:
        verbose_name = "Asset"
        verbose_name_plural = "Assets"

        permissions = [
            ("see_own", "Can see own added assets"),
            ("see_others", "Can see others added assets"),
            ("edit_own", "Can edit own assets"),
            ("edit_others", "Can edit others assets"),
            ("delete_own", "Can delete own assets"),
            ("delete_others", "Can delete others assets"),
            ("upload", "Can upload assets")
        ]

    def content_path(instance, filename):
        print(instance)
        return 'meshes/{0}/{1}'.format(instance.id, filename)

    name = models.TextField()
    description = models.TextField()

    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    last_update = models.DateTimeField(default=datetime.now, blank=True)

    blender_mesh = models.FileField(upload_to=content_path, null=True)
    fbx_mesh = models.FileField(upload_to=content_path, null=True)
    preview_mesh = models.FileField(upload_to=content_path, null=True)

    textures = models.ManyToManyField(Texture)

    tags = models.ManyToManyField(AssetTag)

    favorites = models.ManyToManyField(User, related_name="users_favorites")

    def delete(self, *args, **kwargs):
        self.blender_mesh.delete()
        self.fbx_mesh.delete()
        self.preview_mesh.delete()

        os.rmdir(os.path.abspath(os.path.join(settings.MEDIA_ROOT, 'meshes', str(self.pk))))

        for texture in self.textures.all():
            texture.delete()

        return super().delete(args, kwargs)
