from django.urls import path
from . import views

urlpatterns = [
    path("upload/", views.upload_view, name='upload'),
    path("view/<int:asset_pk>/", views.view_view, name='asset_view'),
    path("view/<int:asset_pk>/add-relation", views.add_relation_action, name='asset_add_relation'),
    path("edit/<int:asset_pk>/", views.edit_view, name='asset_edit'),
    path("delete/<int:asset_pk>/", views.delete_action, name='asset_delete'),
    path("download_asset/<int:asset_pk>/", views.download_asset_zip, name='download_asset'),
    path("download_textures/<int:asset_pk>/", views.download_textures_zip, name='download_textures')
]
