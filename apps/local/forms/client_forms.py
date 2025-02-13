from django import forms
from apps.local.models import Client

        
class CreateClientForm(forms.ModelForm):
    
    class Meta:
        model = Client
        fields = "__all__"

class UpdateClientForm(forms.ModelForm):
    
    class Meta:
        model = Client
        fields = "__all__"
