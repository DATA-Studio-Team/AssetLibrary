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
        return 'assets/{0}_{1}/{2}'.format(instance.card_name, instance.id, filename)

    def texture_content_path(instance, filename):
        return 'assets/{0}_{1}/textures/{2}'.format(instance.card_name, instance.id, filename)

    card_name = models.TextField()
    card_description = models.TextField()

    author = models.ForeignKey(User, on_delete=models.CASCADE)

    blender_mesh = models.FileField(upload_to=mesh_content_path)
    fbx_mesh = models.FileField(upload_to=mesh_content_path)
    preview_mesh = models.FileField(upload_to=mesh_content_path)

    tags = ArrayField(models.ForeignKey(CardTagsModel, on_delete=models.CASCADE))

    textures = ArrayField(models.FileField(upload_to=texture_content_path))