from django.urls import path,include
from apps.account.views.admin_views import change_information
from apps.general.views.general_views import dashboard_view

urlpatterns = [
    path('',dashboard_view,name='dashboard_view'),
    path('admins/',include('apps.account.urls.admin_urls')),
    path('perfil/', change_information, name='change_information'),
]

