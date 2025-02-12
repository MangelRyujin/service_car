from django import forms
from apps.service.models import Service

        
class CreateServiceForm(forms.ModelForm):
    
    class Meta:
        model = Service
        fields = "__all__"

class UpdateServiceForm(forms.ModelForm):
    
    class Meta:
        model = Service
        fields = "__all__"
