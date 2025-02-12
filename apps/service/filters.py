import django_filters
from apps.service.models import Service



class ServiceFilter(django_filters.FilterSet):
    name=  django_filters.CharFilter(lookup_expr='icontains')
    description=  django_filters.CharFilter(lookup_expr='icontains')
    is_active = django_filters.BooleanFilter()
    
    class Meta:
        model = Service
        fields = ['name','description','is_active']
        
