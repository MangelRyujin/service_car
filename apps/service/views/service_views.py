from django.shortcuts import render
from apps.account.decorators import group_required
from django.core.paginator import Paginator
import logging

from apps.account.models import User
from apps.service.filters import ServiceFilter
from apps.service.forms.service_forms import CreateServiceForm, UpdateServiceForm
from apps.service.models import Service
from utils.paginator import _create_paginator
logger = logging.getLogger(__name__)
from django.contrib.admin.views.decorators import staff_member_required

# category view (index)
@group_required('administrador')
@staff_member_required(login_url='/')
def service_view(request):
    response= render(request,'service_templates/service.html')
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

# Charge result table
@staff_member_required(login_url='/')
def service_table_results(request):
    return  render(request,'service_templates/service_table_results.html',context=_show_service(request))
       
# category create form
@staff_member_required(login_url='/')
def service_create(request):
    context={}
    if request.method == "POST":
        form = CreateServiceForm(request.POST)
        if form.is_valid():
            form.save()  
            context['message']='Creado correctamente'
        else:
            context['error']='Corrige los errores'
        context['form']=form
        return render(request,'service_templates/actions/serviceCreate/serviceCreateForm.html',context) 
    form = CreateServiceForm()
    context['form']=form
    return render(request,'service_templates/actions/serviceCreate/serviceCreateForm.html',context) 


# category update forms
@staff_member_required(login_url='/')
def service_update(request,pk):
    service = Service.objects.filter(pk=pk).first()
    form = UpdateServiceForm(instance=service)
    context={}
    context['service']=service
    context['form']=form
    return render(request,'service_templates/actions/serviceUpdate/serviceUpdateForm.html',context) 

# service main information update form
@staff_member_required(login_url='/')
def service_form_update(request,pk):
    context={}
    if request.method == "POST":
        service = Service.objects.filter(pk=pk).first()
        form = UpdateServiceForm(request.POST,request.FILES,instance=service)
        if form.is_valid():
            service_form_valid=form.save(commit=False)
            service_form_valid._change_reason = f'service {service.name} modificado'
            service_form_valid.save()
            form.save_m2m()
            message="Editado correctamente"
            context['message']=message
        else:
            message="Corrige los errores"
            context['error']=message
        context['service']=service
        context['form']=form
        return render(request,'service_templates/actions/serviceUpdate/serviceUpdateCheckForm.html',context) 


# Delete result table
@staff_member_required(login_url='/')
def service_delete(request,pk):
    service = Service.objects.filter(pk=pk).first()
    context={}
    if request.method == "POST":
        if service:
            service_name=service.name
            service.delete()
            context = _show_service(request)
            context['message']=f'service {service_name} ha sido eliminado'
        else:
            context['error']=f'Lo sentimos, el service no existe'
        return render(request,'service_templates/service_table_results.html',context)
    return  render(request,'service_templates/actions/serviceDelete/serviceDeleteVerify.html',{"service":service})
     


# Show service table
@staff_member_required(login_url='/')
def _show_service(request):
    return _create_paginator(request,ServiceFilter(request.GET, queryset=Service.objects.all().order_by('-id')))
