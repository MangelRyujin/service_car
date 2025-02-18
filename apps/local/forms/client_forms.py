from django import forms
from apps.local.models import Client

        
class CreateClientForm(forms.ModelForm):
    
    class Meta:
        model = Client
        exclude = ['count_discount']

class UpdateClientForm(forms.ModelForm):
    
    class Meta:
        model = Client
        exclude = ['count_discount']
