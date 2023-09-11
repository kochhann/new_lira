from django.urls import path
from django.contrib.auth.views import (
    LogoutView
)
from .views import (
    load_cidades,
    IndexView,
    LoginView,
    DashboardView,
    OpUserCreate,
    OpUserList,
    ResetPasswordView,
    ResetPasswordConfirmView,
    ResetPasswordCompleteView,
    CustomerList,
    CustomerCreate,
    CustomerView
)

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
    path('customer/list/', CustomerList.as_view(), name='list_customer'),
    path('customer/create/', CustomerCreate.as_view(), name='create_customer'),
    path('customer/create/load-cidades', load_cidades, name='load_cidades'),
    path('customer/detail/<int:pk>/', CustomerView.as_view(), name='view_customer')
]