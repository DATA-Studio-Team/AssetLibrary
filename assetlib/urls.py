"""assetlib URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.contrib.auth.decorators import login_required
from django.views.static import serve
from main import views
from django.conf import settings
from content.models import Asset, Texture
from django.db.models import Q
from django.http import HttpResponseNotFound

@login_required(login_url='/auth/')
def protected_serve(request, path, document_root=None, show_indexes=False):
    assets = Asset.objects.filter(Q(blender_mesh = path) | Q(fbx_mesh = path) | Q(preview_mesh = path) | Q(textures__in = Texture.objects.filter(texture = path)))

    if not assets.exists():
        return HttpResponseNotFound()

    asset = assets.first()

    if request.user.has_perm("content.see_own"):
        if asset.author.pk == request.user.pk:
            return serve(request, path, document_root, show_indexes)
    
    if request.user.has_perm("content.see_others"):
        if asset.author.pk != request.user.pk:
            return serve(request, path, document_root, show_indexes)

    return HttpResponseNotFound()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.library_view, name='library'),
    path('assets', views.assets_view),
    path('', include('custom_auth.urls')),
    path('', include('content.urls')),

    re_path(r'^%s(?P<path>.*)$' % settings.MEDIA_URL[1:], protected_serve, {'document_root': settings.MEDIA_ROOT}),
]
