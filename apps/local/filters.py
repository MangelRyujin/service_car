import django_filters
from apps.local.models import Client, Local



class LocalFilter(django_filters.FilterSet):
    name=  django_filters.CharFilter(lookup_expr='icontains')
    address=  django_filters.CharFilter(lookup_expr='icontains')
    
    class Meta:
        model = Local
        fields = ['name','address']
        

class ClientFilter(django_filters.FilterSet):
    email=  django_filters.CharFilter(lookup_expr='icontains')
    full_name=  django_filters.CharFilter(lookup_expr='icontains')
    
    class Meta:
        model = Client
        fields = ['email','full_name']