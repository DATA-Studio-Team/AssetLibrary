from django.db import models

class CardTagsCategoriesModel(models.Model):
    category_name = models.CharField(max_length=50)
    order = models.SmallIntegerField(unique=True)

class CardTagsModel(models.Model):
    tag_name = models.CharField(max_length=50)
    category = models.ForeignKey(CardTagsCategoriesModel, on_delete=models.CASCADE)