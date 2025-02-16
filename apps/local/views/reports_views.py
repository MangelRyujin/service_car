from django.shortcuts import render,get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from apps.local.filters import OrderFilter
from apps.local.models import Local, Order
from utils.paginator import _create_paginator


# Reports view 

@staff_member_required(login_url='/login/')
def report_order_view(request):
    context={
        'locals': Local.objects.all().order_by('name'),
        
    }
    response= render(request,'reports_templates/order_templates/order.html',context)
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

# Charge result table
@staff_member_required(login_url='/')
def reports_order_table_results(request):
    return  render(request,'reports_templates/order_templates/order_table_results.html',context=_show_order(request))


# Show order table
@staff_member_required(login_url='/')
def _show_order(request):
    return _create_paginator(request,OrderFilter(request.GET, queryset=Order.objects.filter(is_paid=True).order_by('-id')))


# Detail user order table
@staff_member_required(login_url='/')
def reports_order_detail(request,pk):
    order = get_object_or_404(Order,pk=pk)
    return  render(request,'reports_templates/order_templates/actions/orderDetail/orderDetail.html',{"order":order})
     