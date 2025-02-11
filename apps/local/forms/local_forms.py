from django import forms
from apps.local.models import Local

        
class CreateLocalForm(forms.ModelForm):
    
    class Meta:
        model = Local
        fields = "__all__"

class UpdateLocalForm(forms.ModelForm):
    
    class Meta:
        model = Local
        fields = "__all__"
