from django.db import models
from django.contrib.auth.models import User

class AssetTagCategory(models.Model):

    class Meta:
        verbose_name = "asset_tag_category"
        verbose_name_plural = "asset_tag_categories"

    name = models.CharField(max_length=50)
    order = models.SmallIntegerField(unique=True)

    def __str__(self):
        return self.name

class AssetTag(models.Model):

    class Meta:
        verbose_name = "asset_tag"
        verbose_name_plural = "asset_tags"

    name = models.CharField(max_length=50)
    category = models.ForeignKey(AssetTagCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Texture(models.Model):

    class Meta:
        verbose_name = "texture"
        verbose_name_plural = "textures"

    def content_path(instance, filename):
        return 'textures/{0}/{1}'.format(instance.id, filename)
    
    texture = models.FileField(upload_to=content_path)

class Asset(models.Model):

    class Meta:
        verbose_name = "asset"
        verbose_name_plural = "assets"

    def content_path(instance, filename):
        print(instance)
        return 'assets/{0}/{1}'.format(instance.id, filename)

    name = models.TextField()
    description = models.TextField()

    author = models.ForeignKey(User, on_delete=models.CASCADE)

    blender_mesh = models.FileField(upload_to=content_path, null=True)
    fbx_mesh = models.FileField(upload_to=content_path, null=True)
    preview_mesh = models.FileField(upload_to=content_path, null=True)

    tags = models.ManyToManyField(AssetTag)

    textures = models.ManyToManyField(Texture)
