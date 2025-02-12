from django.shortcuts import render,get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
import logging
from apps.account.decorators import group_required
from apps.local.models import Order
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
        Q(pk__icontains=keyword) ,created_user_pk=str(request.user.pk) ,is_paid=False
        
        ).distinct().order_by('-id')
    context={
        'orders':orders,
        
    }
    return context


# Local order create btn
@group_required('gestor')
@staff_member_required(login_url='/')
def order_create(request):
    context=_show_order_order(request)
    if request.method == "POST":
        local=request.user.local_set.first()
        Order.objects.create(
            local=local,
            created_user_pk = request.user.pk,
            created_user_username = request.user.username,
            created_user_email = request.user.email
        )
    return render(request,'sales/order_result.html',context) 

# Local order create btn
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