from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User
from django.db import models

class CardTagsCategoriesModel(models.Model):
    category_name = models.CharField(max_length=50)
    order = models.SmallIntegerField(unique=True)

class CardTagsModel(models.Model):
    tag_name = models.CharField(max_length=50)
    category = models.ForeignKey(CardTagsCategoriesModel, on_delete=models.CASCADE)

class CardContentModel(models.Model):

    def mesh_content_path(instance, filename):
        print(instance)
        return 'assets/{0}/{1}'.format(instance.id, filename)

    def texture_content_path(instance, filename):
        return 'assets/{0}/textures/{1}'.format(instance.id, filename)

    card_name = models.TextField()
    card_description = models.TextField()

    author = models.ForeignKey(User, on_delete=models.CASCADE)

    blender_mesh = models.FileField(upload_to=mesh_content_path, null=True)
    fbx_mesh = models.FileField(upload_to=mesh_content_path, null=True)
    preview_mesh = models.FileField(upload_to=mesh_content_path, null=True)

    tags = models.ManyToManyField(CardTagsModel)

    textures = ArrayField(models.FileField(upload_to=texture_content_path), null=True)