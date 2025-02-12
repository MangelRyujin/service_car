from django.shortcuts import render,get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
import logging
from apps.account.decorators import group_required
from apps.local.forms.order_forms import CreateExtraItemForm, CreateItemForm, CreateOrderForm, UpdateOrderForm
from apps.local.models import ExtraItem, Item, Order
from apps.service.models import Service
logger = logging.getLogger(__name__)
from django.db.models import Q
from django.utils.translation import gettext as _
  
# order index 
@group_required('administrador','gestor')
@staff_member_required(login_url='/')
def order_view(request):
    context = {'orders':Order.objects.filter(is_paid=False,created_user_pk=str(request.user.pk)).order_by('-id')}
    response= render(request,'sales/order.html',context)
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

# order search result
@staff_member_required(login_url='/')
def order_results_view(request):
    return  render(request,'sales/order_result.html',context=_show_order_order(request))
       
# order search funtion
@staff_member_required(login_url='/')
def _show_order_order(request):
    keyword = request.session.get('keyword', '')
    
    if request.method == 'POST':
        keyword = request.POST.get("keyword",'')
        request.session['keyword'] = keyword

    orders = Order.objects.filter(
        Q(pk__icontains=keyword) | Q(client_email__icontains=keyword) |
        Q(client_full_name__icontains=keyword) | Q(client_car_plaque__icontains=keyword) |
        Q(client_car_brand__icontains=keyword) | Q(client_car_model__icontains=keyword) |
        Q(order_item__service__name__icontains=keyword) | Q(order_extra_item__description__icontains=keyword)
        ,created_user_pk=str(request.user.pk) ,is_paid=False
        
        ).distinct().order_by('-id')
    context={
        'orders':orders,
        
    }
    return context

# Local order detail 
@group_required('gestor')
@staff_member_required(login_url='/')
def order_detail(request,pk):
    context={
        'order': get_object_or_404(Order,pk=pk,created_user_pk = str(request.user.pk))
    }
    if context['order'].is_paid:
        context['order']=[]
    return render(request,'sales/order_component.html',context) 

# Local order create btn
@group_required('gestor')
@staff_member_required(login_url='/')
def order_create(request):
    context=_show_order_order(request)
    if request.method == "POST":
        local=request.user.local_set.first()
        form = CreateOrderForm(request.POST,request.FILES)
        if form.is_valid():
            order = form.save(commit=False)
            order.local=local
            order.created_user_pk=request.user.pk
            order.created_user_username=request.user.username
            order.created_user_email=request.user.email
            order.save()
            context['message']="Orden creada correctamente"
    return render(request,'sales/orderCreate/orderCreateCheckForm.html',context) 

# Local order delete btn
@group_required('gestor')
@staff_member_required(login_url='/')
def order_delete(request,pk):
    order=Order.objects.filter(pk=pk,created_user_pk = str(request.user.pk)).first()
    context={
        'order':order
    }  
    if request.method == "POST":
        order.delete()
        context['order']=[]
        return render(request,'sales/order_component.html',context) 
    return render(request,'sales/orderDelete/orderDeleteVerify.html',context) 

# Local order update
@group_required('gestor')
@staff_member_required(login_url='/')
def order_update(request,pk):
    order=get_object_or_404(Order,pk=pk,created_user_pk = str(request.user.pk))
    context={
        'order':order,
        'form': UpdateOrderForm(instance=order)
        
    }  
    if request.method == "POST":
        form=UpdateOrderForm(request.POST,request.FILES,instance=order)
        if form.is_valid():
            form.save()
            context['message']='Editado correctamente'
        return render(request,'sales/orderUpdate/orderUpdateCheckForm.html',context) 
    return render(request,'sales/orderUpdate/orderUpdateCheckForm.html',context) 

# Local order item create
@group_required('gestor')
@staff_member_required(login_url='/')
def order_item_create(request,pk):
    order = get_object_or_404(Order,pk=pk,created_user_pk = str(request.user.pk))
    form=CreateItemForm()
    context={
        'order': order,
        'services': [service for service in Service.objects.filter(is_active=True).order_by('name') if not order.order_item.filter(service=service)],
        'extra_form':CreateExtraItemForm()
    }   
    if request.method == "POST":
        form= CreateItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.order=order
            item.price=item.service.price
            item.save()
            context['services'].remove(item.service)
            context['message']="Servicio añadido con éxito"
    context['form']=form
    
    return render(request,'sales/serviceOrderUpdate/serviceOrderUpdateCheckForm.html',context) 



# Local order item create
@group_required('gestor')
@staff_member_required(login_url='/')
def order_extra_item_create(request,pk):
    order = get_object_or_404(Order,pk=pk,created_user_pk = str(request.user.pk))
    form=CreateExtraItemForm()
    context={
        'order': order,
        'extra_form':form
    }   
    if request.method == "POST":
        form= CreateExtraItemForm(request.POST)
        if form.is_valid():
            extra_item = form.save(commit=False)
            extra_item.order=order
            extra_item.save()
            context['extra_message']="Servicio extra añadido con éxito"
    context['form']=form
    return render(request,'sales/serviceOrderUpdate/extraServiceOrderUpdateCheckForm.html',context) 


# Local order item delete btn
@group_required('gestor')
@staff_member_required(login_url='/')
def order_item_delete(request,pk):
    item=get_object_or_404(Item,pk=pk)
    order=item.order
    context={
        'order':order
    }  
    if request.method == "POST":
        item.delete()
    return render(request,'sales/order_component.html',context) 

# Local order extra item delete btn
@group_required('gestor')
@staff_member_required(login_url='/')
def order_extra_item_delete(request,pk):
    extra_item=get_object_or_404(ExtraItem,pk=pk)
    order=extra_item.order
    context={
        'order':order
    }  
    if request.method == "POST":
        extra_item.delete()
    return render(request,'sales/order_component.html',context) 

# Local order sold
@group_required('gestor')
@staff_member_required(login_url='/')
def order_sold(request,pk):
    order=get_object_or_404(Order,pk=pk)
    context={
        'order':order
    }  
    if request.method == "POST":
        order.is_paid=True
        order.price = order.total_price
        order.save()
        context['message']="Pago completado con éxito"
    return render(request,'sales/orderSold/orderSoldVerify.html',context) 