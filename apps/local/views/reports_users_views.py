from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from apps.account.decorators import group_required
from apps.account.models import User
from apps.local.filters import ExtraItemsFilter, ItemsFilter
from apps.local.models import ExtraItem, Item, Local


# Reports view 
@group_required('administrador','gestor')
@staff_member_required(login_url='/')
def report_order_users_view(request):
    context={
        'locals': Local.objects.all().order_by('name') if request.user.groups.filter(name__in=['administrador']).exists() else Local.objects.filter(users=request.user).order_by('name'),
        'users' : User.objects.all().order_by('username')
    }
    response= render(request,'reports_templates/reports_user_sales/reports.html',context)
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

# Charge result table
@group_required('administrador','gestor')
@staff_member_required(login_url='/')
def order_users_table_results(request):
    if request.user.groups.filter(name__in=['administrador']).exists():
        service_queryset=Item.objects.filter(order__is_paid=True).order_by('order__client_car_plaque')
        extra_services_queryset=ExtraItem.objects.filter(order__is_paid=True).order_by('order__client_car_plaque')
    else:
        service_queryset=Item.objects.filter(order__is_paid=True,order__created_user_pk=request.user.pk).order_by('order__client_car_plaque')
        extra_services_queryset=ExtraItem.objects.filter(order__is_paid=True,order__created_user_pk=request.user.pk).order_by('order__client_car_plaque')
    services = ItemsFilter(request.GET, queryset=service_queryset).qs
    extra_services = ExtraItemsFilter(request.GET, queryset=extra_services_queryset).qs
    item_total_price = sum(service.price for service in services) or 0
    extra_item_total_price = sum(extra_service.price for extra_service in extra_services) or 0
    total_price = item_total_price + extra_item_total_price
    context={
        'items': services,
        'extra_items':extra_services,
        'item_total_price':item_total_price,
        'item_total_count':services.count(),
        'extra_item_total_price':extra_item_total_price,
        'extra_item_total_count':extra_services.count(),
        'total_price':total_price,
        'total_price_60':(total_price*60)/100,
        'total_price_40':(total_price*40)/100,
    }
    return  render(request,'reports_templates/reports_user_sales/reports_sales_results.html',context)
