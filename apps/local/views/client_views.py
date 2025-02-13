from django.shortcuts import render
from apps.account.decorators import group_required
from django.core.paginator import Paginator
import logging

from apps.account.models import User
from apps.local.filters import LocalFilter
from apps.local.forms.client_forms import CreateClientForm
from apps.local.models import Local,Client
from utils.paginator import _create_paginator
logger = logging.getLogger(__name__)
from django.contrib.admin.views.decorators import staff_member_required

# category create form
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

