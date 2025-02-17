from django.shortcuts import render,get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
import logging
from django.forms import modelformset_factory
from apps.account.decorators import group_required
from apps.local.forms.client_forms import CreateClientForm
from apps.local.forms.order_forms import CreateExtraItemForm, CreateItemForm, CreateOrderForm, ExtraItemMarksForm,  ItemMarksForm, OrderDiscountForm, UpdateExtraItemForm, UpdateOrderForm
from apps.local.models import Client, ExtraItem, Item, Order
from apps.local.utils.order_create import create_order
from apps.service.models import Service
logger = logging.getLogger(__name__)
from django.db.models import Q
from django.utils.translation import gettext as _
from django.db import transaction, IntegrityError
  
# order index 
@group_required('administrador','gestor')
@staff_member_required(login_url='/')
def order_view(request):
    context = {
        'orders':Order.objects.filter(is_paid=False,created_user_pk=str(request.user.pk)).order_by('-id'),
        'clients': Client.objects.all(),
        'client_form': CreateClientForm()
               }
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
        Q(pk__icontains=keyword) | Q(client__email__icontains=keyword) |
        Q(client__full_name__icontains=keyword) | Q(client_car_plaque__icontains=keyword) |
        Q(order_item__service__name__icontains=keyword) | Q(order_extra_item__description__icontains=keyword)
        ,created_user_pk=str(request.user.pk) ,is_paid=False
        
        ).distinct().order_by('-id')
    context={
        'orders':orders,
        
    }
    return context

#  order detail 
@group_required('administrador','gestor')
@staff_member_required(login_url='/')
def order_detail(request,pk):
    context={
        'order': get_object_or_404(Order,pk=pk,created_user_pk = str(request.user.pk))
    }
    if context['order'].is_paid:
        context['order']=[]
    return render(request,'sales/order_component.html',context) 



      
#  order create btn
@group_required('administrador','gestor')
@staff_member_required(login_url='/')
def order_create(request):
    context={}
    MarksFormset = modelformset_factory(Item, form=ItemMarksForm)
    formset = MarksFormset(queryset= Item.objects.none(), prefix='items')
    ExtraMarksFormset = modelformset_factory(ExtraItem, form=ExtraItemMarksForm)
    extra_formset=ExtraMarksFormset(queryset= ExtraItem.objects.none(), prefix='extraitems')
    form = CreateOrderForm()
    if request.method == "POST":
        extra_formset = ExtraMarksFormset(request.POST or None, queryset= ExtraItem.objects.none(), prefix='extraitems')
        formset = MarksFormset(request.POST or None, queryset= Item.objects.none(), prefix='items')
        form = CreateOrderForm(request.POST or None,request.FILES)
        local=request.user.local_set.first() 
        if form.is_valid() and formset.is_valid() and extra_formset.is_valid():
                try:
                    with transaction.atomic():
                        create_order(request,form,local,formset,extra_formset)
                        form = CreateOrderForm()
                        context['message']="Orden creada correctamente"
                        formset = MarksFormset(queryset= Item.objects.none(), prefix='items')
                        extra_formset=ExtraMarksFormset(queryset= ExtraItem.objects.none(), prefix='extraitems')
                except IntegrityError:
                    pass
                
    context['clients']=Client.objects.all()
    context['services']=Service.objects.filter(is_active=True).order_by('name')
    context['formset'] = formset
    context['extra_formset'] = extra_formset
    context['form'] = form
    return render(request,'sales/orderCreate/orderCreateCheckForm.html',context) 


#  order delete btn
@group_required('administrador','gestor')
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

#  order update
@group_required('administrador','gestor')
@staff_member_required(login_url='/')
def order_update(request,pk):
    order=get_object_or_404(Order,pk=pk,created_user_pk = str(request.user.pk))
    
    context={
        'order':order,
        'form': UpdateOrderForm(instance=order),
        'clients': Client.objects.all(),
        'services':Service.objects.filter(is_active=True),
        'item_form': CreateItemForm(),
        'extra_form': CreateExtraItemForm()
    }
    
    if request.method == "POST":
        form=UpdateOrderForm(request.POST,request.FILES,instance=order)
        if form.is_valid():
            form.save()
            context['message']='Editado correctamente'
        return render(request,'sales/orderUpdate/orderUpdateCheckForm.html',context) 
    return render(request,'sales/orderUpdate/orderUpdateCheckForm.html',context) 



#  order item create
@group_required('administrador','gestor')
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



#  order item create
@group_required('administrador','gestor')
@staff_member_required(login_url='/')
def update_order_item_create(request,pk):
    order = get_object_or_404(Order,pk=pk,created_user_pk = str(request.user.pk))
    form=CreateItemForm()
    context={
        'order': order,
        'services': Service.objects.filter(is_active=True).order_by('name') ,
        
    }   
    if request.method == "POST":
        form= CreateItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.order=order
            item.price=item.service.price
            item.save()
            context['message']="Servicio añadido con éxito"
    context['item_form']=form
    
    return render(request,'sales/orderUpdate/orderUpdateItems.html',context) 



#  order item create
@group_required('administrador','gestor')
@staff_member_required(login_url='/')
def update_order_extra_item_create(request,pk):
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
            context['extra_message_create']="Servicio extra añadido con éxito"
    context['form']=form
    return render(request,'sales/orderUpdate/orderUpdateExtraItems.html',context) 


#  order item create
@group_required('administrador','gestor')
@staff_member_required(login_url='/')
def update_order_extra_item_update(request,pk):
    extra_item = get_object_or_404(ExtraItem,pk=pk)
    form=UpdateExtraItemForm()
    context={
        'order': extra_item.order,
        'extra_item':extra_item
    }   
    if request.method == "POST":
        form= UpdateExtraItemForm(request.POST,instance=extra_item)
        if form.is_valid():
            extra_item = form.save()
            context['extra_message_update']="Servicio editado correctamente"
    context['form']=form
    return render(request,'sales/orderUpdate/extraItemForm.html',context) 


#  order item create
@group_required('administrador','gestor')
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


#  order item delete btn
@group_required('administrador','gestor')
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


@group_required('administrador','gestor')
@staff_member_required(login_url='/')
def update_order_item_delete(request,pk):
    item=get_object_or_404(Item,pk=pk)
    order=item.order
    context={
        'order':order,
        'services':Service.objects.filter(is_active=True),
        'item_form': CreateItemForm()
    }  
    if request.method == "POST":
        item.delete()
        context['message']='Editando servicios correctamente'
    return render(request,'sales/orderUpdate/orderUpdateItems.html',context)

#  order extra item delete btn
@group_required('administrador','gestor')
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

#  order extra item delete btn
@group_required('administrador','gestor')
@staff_member_required(login_url='/')
def update_order_extra_item_delete(request,pk):
    extra_item=get_object_or_404(ExtraItem,pk=pk)
    order=extra_item.order
    context={
        'order':order,
        'extra_item':extra_item
    }  
    if request.method == "POST":
        extra_item.delete()
        context['extra_item']=[]
        context['extra_item_message_delete']="Servicio extra eliminado correctamente"
    return render(request,'sales/orderUpdate/extraItemForm.html',context) 



#  order sold
@group_required('administrador','gestor')
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
        if order.client and order.discount > 0:
            order.client.count_discount=0
            order.client.save()
        context['message']="Pago completado con éxito"
    return render(request,'sales/orderSold/orderSoldVerify.html',context) 

# order discount
@group_required('administrador','gestor')
@staff_member_required(login_url='/')
def order_discount(request,pk):
    order = get_object_or_404(Order,pk=pk,is_paid=False)
    context = {
        'order': order,
        'discount_form': OrderDiscountForm(instance=order) if order.client and order.client.count_discount > 4 else None
    }
    if request.method == "POST":
            form = OrderDiscountForm(request.POST,instance=order)
            if form.is_valid():
                form.save()
                context['message']="Descuento añadido correctamente"
            else:
                pass

    return render(request,'sales/orderDiscount/orderDiscountForm.html',context) 