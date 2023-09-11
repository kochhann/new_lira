from django.contrib import admin
from .models import EquipamentType

@admin.register(EquipamentType)
class EquipamentTypeAdmin(admin.ModelAdmin):
    list_display = ['brand', 'model']
