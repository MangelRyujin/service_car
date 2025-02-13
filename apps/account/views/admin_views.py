from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.models import Group
from apps.account.decorators import group_required
from apps.account.models import User
from apps.account.filters import AdminFilter
from apps.account.forms.admin_forms import  SingUpForm,ChangeAdminForm,ChangeUserPersonalInformation
from django.contrib.auth.forms import AdminPasswordChangeForm
import logging

from apps.local.forms.client_forms import CreateClientForm
from utils.paginator import _create_paginator


logger = logging.getLogger(__name__)
from django.contrib.admin.views.decorators import staff_member_required

# admin view (index)
@group_required('administrador')
@staff_member_required(login_url='/')
def admin_view(request):
    
    context={
        'client_form': CreateClientForm(),
        'groups' : Group.objects.all()
    }
    response= render(request,'admin_templates/admin.html',context)
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

# Charge result table
@group_required('administrador')
@staff_member_required(login_url='/')
def admin_table_results(request):
    return  render(request,'admin_templates/admin_table_results.html',context=_show_admin(request))
       
# admin create form
@group_required('administrador')
@staff_member_required(login_url='/')
def admin_create(request):
    form = SingUpForm(request.POST or None)
    groups = Group.objects.all()
    context={
        'form':form,
        'groups':groups
    }
    if request.method == "POST":
        if form.is_valid():
            admin_form_valid=form.save(commit=False)
            admin_form_valid.is_staff=True
            admin_form_valid.save()  
            form.save_m2m()
            context['message']='Creado correctamente'
        else:
            context['error']='Corrige los errores'
    return render(request,'admin_templates/actions/adminCreate/adminCreateForm.html',context) 


# admin update forms
@group_required('administrador')
@staff_member_required(login_url='/')
def admin_update(request,pk):
    admin = User.objects.filter(pk=pk).first()
    form = ChangeAdminForm(instance=admin)
    pass_form = AdminPasswordChangeForm(user=admin)
    context={}
    context['admin']=admin
    context['form']=form
    context['pass_form']=pass_form
    return render(request,'admin_templates/actions/adminUpdate/adminUpdateForm.html',context) 

# admin main information update form
@group_required('administrador')
@staff_member_required(login_url='/')
def admin_main_information_update(request,pk):
    context={}
    if request.method == "POST":
        admin = User.objects.filter(pk=pk).first()
        form = ChangeAdminForm(request.POST,request.FILES,instance=admin)
        if form.is_valid():
            admin_form_valid=form.save(commit=False)
            # admin_form_valid._change_reason = f'Modifying personal information for the {admin.username} administrator'
            admin_form_valid.save()
            form.save_m2m()
            message="Editado correctamente"
            context['message']=message
        else:
            message="Corrige los errores"
            context['error']=message
        context['admin']=admin
        context['form']=form
        return render(request,'admin_templates/actions/adminUpdate/mainAdminUpdate.html',context) 


# admin password update form
@group_required('administrador')
@staff_member_required(login_url='/')
def admin_password_update(request,pk):
    context={}
    if request.method == "POST":
        admin = User.objects.filter(pk=pk).first()
        pass_form = AdminPasswordChangeForm(admin,request.POST)
        if pass_form.is_valid():
            admin_form_valid = pass_form.save(commit=False)
            # admin_form_valid._change_reason = f"Modifying the password for the {admin.username} administrator"
            admin_form_valid.save()
            message="Editado correctamente"
            context['message']=message
        else:
            message="Corrige los errores"
            context['error']=message
        context['admin']=admin
        context['pass_form']=pass_form
        return render(request,'admin_templates/actions/adminUpdate/passAdminUpdate.html',context) 


# Delete result table
@group_required('administrador')
@staff_member_required(login_url='/')
def admin_delete(request,pk):
    admin = User.objects.filter(pk=pk).first()
    context={}
    if request.method == "POST":
        if admin:
            admin_name=admin.username
            admin.delete()
            context = _show_admin(request)
            context['message']=f'{admin_name} ha sido eliminado'
        else:
            context['error']=f'Lo sentimos, el administrador no existe'
        return render(request,'admin_templates/admin_table_results.html',context)
    return  render(request,'admin_templates/actions/adminDelete/adminDeleteVerify.html',{"admin":admin})
     


# Show admin table
@group_required('administrador')
@staff_member_required(login_url='/')
def _show_admin(request):
    return _create_paginator(request,AdminFilter(request.GET, queryset=User.objects.exclude(is_staff=False).order_by('-id')))


# Detail user admin table
@group_required('administrador')
@staff_member_required(login_url='/')
def admin_detail(request,pk):
    admin = User.objects.filter(pk=pk).first()
    return  render(request,'admin_templates/actions/adminDetail/adminDetail.html',{"admin":admin})

# Change Personal Information of user admins
def change_information(request):
    user = User.objects.get(pk=request.user.pk)
    if request.method == 'POST':
        form = ChangeUserPersonalInformation(request.POST, instance=user)
        if form.is_valid():
            admin_form = form.save(commit=False)
         
            admin_form.save()
        context = {"form": form,
                   "message":"Perfil editado correctamente"
                    }
        return render(request,'admin_templates/actions/adminInformation/adminInformationUpdateForm.html', context)
    form = ChangeUserPersonalInformation(instance=user)
    context = {
        "form": form,
        
        }
    return render(request, 'admin_templates/actions/adminInformation/adminInformation.html', context)