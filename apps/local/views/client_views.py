from django.shortcuts import render,get_object_or_404
from apps.account.decorators import group_required
import logging
from apps.local.filters import ClientFilter
from apps.local.forms.client_forms import CreateClientForm, UpdateClientForm
from apps.local.models import Local,Client
from utils.paginator import _create_paginator
logger = logging.getLogger(__name__)
from django.contrib.admin.views.decorators import staff_member_required


# local view (index)
@group_required('administrador')
@staff_member_required(login_url='/')
def client_view(request):
    response= render(request,'client_templates/client.html',{'client_form':CreateClientForm()})
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

# Charge result table
@group_required('administrador')
@staff_member_required(login_url='/')
def client_table_results(request):
    return  render(request,'client_templates/client_table_results.html',context=_show_client(request))


# client create form
@group_required('administrador','gestor')
@staff_member_required(login_url='/')
def client_create(request):
    context={
        'client_form':CreateClientForm()
    }
    if request.method == "POST":
        form = CreateClientForm(request.POST)
        if form.is_valid():
            form.save()  
            context['message']='Cliente creado correctamente'
        context['client_form']=form
    return render(request,'clientCreate/clientCreateForm.html',context) 

# client update forms
@group_required('administrador')
@staff_member_required(login_url='/')
def client_update(request,pk):
    client = get_object_or_404(Client,pk=pk)
    form = UpdateClientForm(instance=client)
    context={
    }
    if request.method == "POST":
        form = UpdateClientForm(request.POST,instance=client)
        if form.is_valid():
            form.save()
            context['message']='Editado correctamente'
        else:
            message="Corrige los errores"
            context['error']=message
    context['client']=client
    context['form']=form
    return render(request,'client_templates/actions/clientUpdate/clientUpdateCheckForm.html',context) 

# Show client table
@group_required('administrador')
@staff_member_required(login_url='/')
def _show_client(request):
    return _create_paginator(request,ClientFilter(request.GET, queryset=Client.objects.all().order_by('email')))