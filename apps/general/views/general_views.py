from django.shortcuts import render
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import authenticate, login 
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordChangeForm
from apps.account.decorators import user_is_not_authenticated
from django.contrib.admin.views.decorators import staff_member_required

from apps.local.forms.client_forms import CreateClientForm


# Dashboard view (index)

@staff_member_required(login_url='/login/')
def dashboard_view(request):
    context={
        'client_form': CreateClientForm()
    }
    response= render(request,'index.html',context)
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response


# Log in view
@user_is_not_authenticated
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        next_url =  request.POST.get('next','')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            response = HttpResponse()
            response["HX-Redirect"]= next_url
            return response
        else:
            return HttpResponse(f"""
                                 <div class="alert alert-dismissible alert-danger d-flex align-items-center mb-0 mt-4 px-2 fade show" role="alert">
                      
                        <div class="small px-1 me-2 text-danger-emphasis">
                          Credenciales incorrectas
                        </div>
                        <span type="button" class="btn-close px-2" data-bs-dismiss="alert" aria-label="Close"></span>
                      </div>
                                
                                """)
    context = {
        "next":request.GET.get('next', ''),
    }
    return render(request, 'login.html',context)


# Change password view
@login_required(login_url='/login/')
def change_password_view(request):
    context = {
        "form":PasswordChangeForm(user=request.user),
    }
    response= render(request, 'change_password/change_password.html',context)
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

# Change password form component
@login_required(login_url='/login/')
def change_password_form(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            response = HttpResponse()
            response["HX-Redirect"]= '/login/'
            return response
        else:
            return render(request, 'change_password/change_password_form.html',{"form":form})
        
