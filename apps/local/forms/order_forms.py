from django import forms
from apps.local.models import ExtraItem, Item, Order



class UpdateOrderForm(forms.ModelForm):
    
    class Meta:
        model = Order
        fields = ['client_email','client_full_name','client_car_plaque','client_car_brand','client_car_model','image']

class CreateItemForm(forms.ModelForm):
    
    class Meta:
        model = Item
        fields = ['service']
        
class CreateExtraItemForm(forms.ModelForm):
    
    class Meta:
        model = ExtraItem
        fields = ['description','price']