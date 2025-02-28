from django.urls import path,include
from apps.account.views.admin_views import change_information
from apps.general.views.general_views import dashboard_view

urlpatterns = [
    path('',dashboard_view,name='dashboard_view'),
    path('admins/',include('apps.account.urls.admin_urls')),
    path('locals/',include('apps.local.urls.local_urls')),
    path('services/',include('apps.service.urls.service_urls')),
    path('perfil/', change_information, name='change_information'),
    path('sales/',include('apps.local.urls.order_urls')),
    path('clients/',include('apps.local.urls.client_urls')),
    path('all_orders/',include('apps.local.urls.reports_order_urls')),
    path('local_orders/',include('apps.local.urls.reports_order_users_urls')),

]

