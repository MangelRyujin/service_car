from django import forms
from apps.local.models import ExtraItem, Item, Order

class CreateOrderForm(forms.ModelForm):
    
    class Meta:
        model = Order
        fields = ['client','client_car_plaque','image']

class UpdateOrderForm(forms.ModelForm):
    
    class Meta:
        model = Order
        fields = ['client','client_car_plaque','image']
        
class OrderDiscountForm(forms.ModelForm):
    
    class Meta:
        model = Order
        fields = ['discount']

class CreateItemForm(forms.ModelForm):
    
    class Meta:
        model = Item
        fields = ['service']
        
class CreateExtraItemForm(forms.ModelForm):
    
    class Meta:
        model = ExtraItem
        fields = ['description','price']
        
        
class ItemMarksForm(forms.ModelForm):
	class Meta:
		model = Item
        
		fields = [
			'service',
		]

		widgets = {
			'service': forms.Select(attrs={'class': 'formset-field'}),
		}
       
class ExtraItemMarksForm(forms.ModelForm):
	class Meta:
		model = ExtraItem
        
		fields = [
			'description',
            'price'
		]

		widgets = {
			'service': forms.CharField(max_length=500),
            'price': forms.NumberInput(
               ),
		}