from django.contrib import admin
from .models import *

@admin.register(EquipamentType)
class EquipamentTypeAdmin(admin.ModelAdmin):
    list_display = ['brand', 'model']

@admin.register(EquipamentBrand)
class EquipamentBrandAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Equipament)
class EquipamentAdmin(admin.ModelAdmin):
    list_display = ['serial_number']
