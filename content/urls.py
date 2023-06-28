from django.urls import path
from . import views

urlpatterns = [
    path("upload/", views.upload_view, name='upload'),
    path("view/<int:asset_pk>", views.view_view, name='asset_view'),
]
