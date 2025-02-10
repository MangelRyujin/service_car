import django_filters
from django.contrib.auth.models import Group
from apps.account.models import User


class AdminFilter(django_filters.FilterSet):
    email=  django_filters.CharFilter(lookup_expr='icontains')
    username=  django_filters.CharFilter(lookup_expr='icontains')
    dni=  django_filters.CharFilter(lookup_expr='icontains')
    is_active = django_filters.BooleanFilter()
    phone_number=  django_filters.CharFilter(lookup_expr='icontains')
    groups = django_filters.ModelMultipleChoiceFilter(queryset=Group.objects.all())


    class Meta:
        model = User
        fields = ['email','dni','groups','username','is_active','is_staff','phone_number']

            
class UserFilter(django_filters.FilterSet):
    email=  django_filters.CharFilter(lookup_expr='icontains')
    phone_number =  django_filters.CharFilter(lookup_expr='icontains')
    username=  django_filters.CharFilter(lookup_expr='icontains')
    is_active = django_filters.BooleanFilter()
    dni=  django_filters.CharFilter(lookup_expr='icontains')
    


    class Meta:
        model = User
        fields = ['email','dni','phone_number','username','is_active']

            