from django.db import models
from django.contrib.auth.models import User

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

class Asset(models.Model):

    class Meta:
        verbose_name = "Asset"
        verbose_name_plural = "Assets"

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
