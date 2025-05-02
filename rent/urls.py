from django.urls import path
from .views import *

urlpatterns = [
    path('', RentIndexView.as_view(), name='rent_index'),
    path('contract/list/<int:type_of>', ContractList.as_view(), name='list_contract'),
    path('contract/create/<int:type_of>', ContractCreate.as_view(), name='create_contract'),
]