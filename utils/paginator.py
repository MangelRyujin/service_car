

from apps.account.models import User
from apps.account.filters import AdminFilter

from django.core.paginator import Paginator

def _create_paginator(request,objects_model):
    get_copy = request.GET.copy()
    parameters = get_copy.pop('page', True) and get_copy.urlencode()
    objects = AdminFilter(request.GET, queryset=objects_model)
    paginator = Paginator(objects.qs, 100)    # Show 25 contacts per page.
    page_number = request.GET.get("page",1)
    page_obj = paginator.get_page(page_number)
    context={
        'pagination':page_obj,
        'parameters': parameters,
    }
    return context