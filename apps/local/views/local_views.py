from django.shortcuts import render
from apps.account.decorators import group_required
from django.core.paginator import Paginator
import logging

from apps.account.models import User
from apps.local.filters import LocalFilter
from apps.local.forms.local_forms import CreateLocalForm, UpdateLocalForm
from apps.local.models import Local
from utils.paginator import _create_paginator
logger = logging.getLogger(__name__)
from django.contrib.admin.views.decorators import staff_member_required

# category view (index)
@group_required('administrador')
@staff_member_required(login_url='/')
def local_view(request):
    response= render(request,'local_templates/local.html')
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

# Charge result table
@staff_member_required(login_url='/')
def local_table_results(request):
    return  render(request,'local_templates/local_table_results.html',context=_show_local(request))
       
# category create form
@staff_member_required(login_url='/')
def local_create(request):
    context={
        'users':User.objects.filter(is_active=True,is_staff=True)
    }
    if request.method == "POST":
        form = CreateLocalForm(request.POST)
        if form.is_valid():
            form.save()  
            context['message']='Creado correctamente'
        else:
            context['error']='Corrige los errores'
        context['form']=form
        return render(request,'local_templates/actions/localCreate/localCreateForm.html',context) 
    form = CreateLocalForm()
    context['form']=form
    return render(request,'local_templates/actions/localCreate/localCreateForm.html',context) 


# category update forms
@staff_member_required(login_url='/')
def local_update(request,pk):
    local = Local.objects.filter(pk=pk).first()
    form = UpdateLocalForm(instance=local)
    context={
        'users':User.objects.filter(is_active=True,is_staff=True)
    }
    context['local']=local
    context['form']=form
    return render(request,'local_templates/actions/localUpdate/localUpdateForm.html',context) 

# local main information update form
@staff_member_required(login_url='/')
def local_form_update(request,pk):
    context={
        'users':User.objects.filter(is_active=True,is_staff=True)
    }
    if request.method == "POST":
        local = Local.objects.filter(pk=pk).first()
        form = UpdateLocalForm(request.POST,request.FILES,instance=local)
        if form.is_valid():
            local_form_valid=form.save(commit=False)
            local_form_valid._change_reason = f'Local {local.name} modificado'
            local_form_valid.save()
            form.save_m2m()
            message="Editado correctamente"
            context['message']=message
        else:
            message="Corrige los errores"
            context['error']=message
        context['local']=local
        context['form']=form
        return render(request,'local_templates/actions/localUpdate/localUpdateCheckForm.html',context) 


# Delete result table
@staff_member_required(login_url='/')
def local_delete(request,pk):
    local = Local.objects.filter(pk=pk).first()
    context={}
    if request.method == "POST":
        if local:
            local_name=local.name
            local.delete()
            context = _show_local(request)
            context['message']=f'Local {local_name} ha sido eliminado'
        else:
            context['error']=f'Lo sentimos, el local no existe'
        return render(request,'local_templates/local_table_results.html',context)
    return  render(request,'local_templates/actions/localDelete/localDeleteVerify.html',{"local":local})
     


# Show local table
@staff_member_required(login_url='/')
def _show_local(request):
    return _create_paginator(request,LocalFilter(request.GET, queryset=Local.objects.all().order_by('-id')))
