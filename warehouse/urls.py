from django.urls import path
from .views import (
    EquipamentTypeCreate,
    EquipamentTypeList,
    EquipamentTypeView
)

urlpatterns = [
    path('equip_type/create/', EquipamentTypeCreate.as_view(), name='create_equipament_type'),
    path('equip_type/list/', EquipamentTypeList.as_view(), name='list_equipament_type'),
    path('equip_type/detail/<int:pk>/', EquipamentTypeView.as_view(), name='view_equipament_type')
]