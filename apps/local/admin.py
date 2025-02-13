from django.contrib import admin

from apps.local.models import *

# Register your models here.

admin.site.register(Local)

class ItemInline(admin.TabularInline):
    model = Item
    extra = 0

class ExtraItemInline(admin.TabularInline):
    model = ExtraItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['pk', 'created_at', 'client','client_car_plaque', 'local','is_paid','price']
    list_per_page = 200
    inlines = [ItemInline,ExtraItemInline]