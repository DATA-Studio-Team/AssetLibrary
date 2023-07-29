from django import forms

class UploadForm(forms.Form):
    card_name = forms.CharField(initial="")
    card_description = forms.CharField(initial="")

    blender_mesh = forms.FileField(required=False)
    fbx_mesh = forms.FileField(required=False)
    preview_mesh = forms.FileField(required=False)

    textures = forms.FileField(required=False)