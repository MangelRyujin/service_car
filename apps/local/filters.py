from apps.account.models import User
import django_filters
from apps.local.models import Client, Item, Local, Order



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
        

class OrderFilter(django_filters.FilterSet):
    created_user_username=django_filters.CharFilter(lookup_expr='icontains')
    client = django_filters.CharFilter(field_name='client__email',lookup_expr='icontains')
    service = django_filters.CharFilter(
        method='filter_by_service',
        lookup_expr='icontains'
    )
    extra_service=django_filters.CharFilter(
        method='filter_by_extra_service',
        lookup_expr='icontains'
    )
    local = django_filters.ModelMultipleChoiceFilter(queryset=Local.objects.all())
    client_car_plaque=django_filters.CharFilter(lookup_expr='icontains')
    created_at =django_filters.DateFromToRangeFilter()
    id = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Order
        fields = ['id','client','created_user_username','local','client_car_plaque','extra_service','created_at']
    
    def filter_by_service(self, qs, name, value):
        return qs.filter(order_item__service__name__icontains=value)
    
    def filter_by_extra_service(self, qs, name, value):
        return qs.filter(order_extra_item__description__icontains=value)
        
        
class ItemsFilter(django_filters.FilterSet):
    local = django_filters.CharFilter(
        method='filter_by_local',
        lookup_expr='exact'
    )
    user = django_filters.CharFilter(
        method='filter_by_created_user_pk',
        lookup_expr='exact'
    )
    created_at =django_filters.DateFromToRangeFilter(field_name='order__created_at')
    
    class Meta:
        model = Item
        fields = ['local','user','created_at']
        
    def filter_by_local(self, qs, name, value):
        return qs.filter(order__local__pk=value)
    
    def filter_by_created_user_pk(self, qs, name, value):
        return qs.filter(order__created_user_pk=value)
    
    
class ExtraItemsFilter(django_filters.FilterSet):
    local = django_filters.CharFilter(
        method='filter_by_extra_local',
        lookup_expr='exact'
    )
    user = django_filters.CharFilter(
        method='filter_by_extra_created_user_pk',
        lookup_expr='exact'
    )
    created_at =django_filters.DateFromToRangeFilter(field_name='order__created_at')
    
    class Meta:
        model = Item
        fields = ['local','user','created_at']
        
    def filter_by_extra_local(self, qs, name, value):
        return qs.filter(order__local__pk=value)
    
    def filter_by_extra_created_user_pk(self, qs, name, value):
        return qs.filter(order__created_user_pk=value)
    
    