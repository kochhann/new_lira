from django.contrib import admin
from .models import (
    HeadCompany,
    Branch,
    OpUser,
    Customer,
    Address,
    Email,
    Telephone
)


@admin.register(HeadCompany)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(OpUser)
class OpUserAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Telephone)
class TelephoneAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    list_display = ['name']
