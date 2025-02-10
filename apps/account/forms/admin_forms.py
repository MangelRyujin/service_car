from django import forms
from apps.account.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

# from apps.accounts.models import Profile

        
class SingUpForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ['username','email','groups','password1','password2']
        
        
class ChangeAdminForm(UserChangeForm):
    class Meta:
        model = User
        exclude = ['password','user_permissions','date_joined','last_login','is_superuser','is_staff']

class ChangeUserPersonalInformation(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name','dni','phone_number','country','city','address']