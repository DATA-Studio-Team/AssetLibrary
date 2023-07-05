from django.urls import path
from . import views

urlpatterns = [
    path("upload/", views.upload_view, name='upload'),
    path("view/<int:asset_pk>", views.view_view, name='asset_view'),
    path("download_textures/<int:asset_pk>", views.download_textures_zip, name='download_textures')
]
