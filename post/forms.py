from django import forms
from post.models import keyfield

class FileUploadForm(forms.Form):
    class Meta:
        model = keyfield
        fields = ['skey']

        
        