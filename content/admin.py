from django.contrib import admin
from .models import *

admin.site.register(AssetTag)
admin.site.register(AssetTagCategory)

admin.site.register(Asset)
admin.site.register(Texture)