from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(min_length=3, max_length=30, initial="")
    password = forms.CharField(min_length=8, max_length=100, initial="")

class UploadForm(forms.Form):
    card_name = forms.CharField(min_length=3, max_length=50, initial="")
    card_description = forms.CharField(min_length=0, max_length=500, initial="")

    blender_mesh = forms.FileField()
    fbx_mesh = forms.FileField()
    preview_mesh = forms.FileField()

   #tags = forms.MultipleChoiceField()

   #textures = forms.FileField()