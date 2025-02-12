from django.urls import path
from apps.local.views.order_views import *

urlpatterns = [
    path('',order_view,name='order_view'),
    path('order_results_view',order_results_view,name='order_results_view'),
    path('order_create',order_create,name='order_create'),
    path('order_delete/<int:pk>/',order_delete,name='order_delete')
]

