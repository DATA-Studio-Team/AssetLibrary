from django import forms

class UploadForm(forms.Form):
    card_name = forms.CharField(min_length=3, max_length=50, initial="")
    card_description = forms.CharField(min_length=0, max_length=500, initial="")

    blender_mesh = forms.FileField()
    fbx_mesh = forms.FileField(required=False)
    preview_mesh = forms.FileField(required=False)

   #tags = forms.MultipleChoiceField()

    textures = forms.FileField(required=False)