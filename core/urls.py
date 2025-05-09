from django.urls import path
from django.contrib.auth.views import (
    LogoutView
)
from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('password-reset/', ResetPasswordView.as_view(), name='password-reset'),
    path('password-reset-confirm/<uidb64>/<token>/', ResetPasswordConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset-complete/', ResetPasswordCompleteView.as_view(), name='password_reset_complete'),
    path('user/create/', OpUserCreate.as_view(), name='create_user'),
    path('user/list/', OpUserList.as_view(), name='list_user'),
    path('customer/list/<int:list_type>', CustomerList.as_view(), name='list_customer'),
    path('customer/create/', CustomerCreate.as_view(), name='create_customer'),
    path('customer/create/load-cidades', load_cidades, name='load_cidades'),
    path('customer/detail/<int:pk>/load-cidades-oncreate', load_cidades_oncreate, name='load_cidades_oncreate'),
    path('customer/detail/<int:pk>/', CustomerView.as_view(), name='view_customer'),
    path('customer/search/', SearchCustomerView.as_view(), name='search_customer'),
    path('customer/update-accoutable/<int:pk>/', UpdateCustAccountable.as_view(), name='update_customer_accountable'),
    path('customer/update-acc-id/<int:pk>/', UpdateCustAccID.as_view(), name='update_customer_acc_id'),
    path('customer/update-name/<int:pk>/', UpdateCustName.as_view(), name='update_customer_name'),
    path('customer/update-corp-name/<int:pk>/', UpdateCustCorpName.as_view(), name='update_customer_corp_name'),
    path('customer/update-st-subscription/<int:pk>/', UpdateCustStSubscription.as_view(), name='update_customer_st_subscription'),
    path('customer/update-cy-subscription/<int:pk>/', UpdateCustCySubscription.as_view(), name='update_customer_cy_subscription'),
    path('customer/update-site/<int:pk>/', UpdateCustSite.as_view(), name='update_customer_site'),
    path('customer/update-observation/<int:pk>/', UpdateCustObservation.as_view(), name='update_customer_observation'),
    path('customer/contact/create/<int:pk>/', ContactCreate.as_view(), name='customer_contact_create'),
    path('customer/address/create/<int:pk>/', AddressCreate.as_view(), name='customer_address_create')
]