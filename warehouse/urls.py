from django.urls import path
from .views import *

urlpatterns = [
    path('', WarehouseIndexView.as_view(), name='wh_index'),
    path('equip_type/create/', EquipamentTypeCreate.as_view(), name='create_equipament_type'),
    path('equip_type/list/', EquipamentTypeList.as_view(), name='list_equipament_type'),
    path('equip_type/detail/<int:pk>/', EquipamentTypeView.as_view(), name='view_equipament_type'),
    path('equip_type/delete/<int:pk>/', EquipamentTypeDelete.as_view(), name='delete_equipament_type'),
    path('equip_type/reactivate/<int:pk>/', EquipamentTypeReactivation.as_view(), name='react_equipament_type'),
    path('equip_brand/create/', EquipamentBrandCreate.as_view(), name='create_equipament_brand'),
    path('equip_brand/list/', EquipamentBrandList.as_view(), name='list_equipament_brand'),
    path('equip_brand/delete/<int:pk>/', EquipamentBrandDelete.as_view(), name='delete_equipament_brand'),
    path('equip_brand/crete_almost_same/<slug:new_brand>/', EquipamentBrandAlmostSameCreate.as_view(),
         name='create_almost_same_brand'),
    path('equip_type/update/<int:pk>/', EquipamentTypeUpdate.as_view(), name='update_equipament_type'),
    path('equipament/list/<int:pk>/<int:many>', EquipamentList.as_view(), name='list_equipament'),
    path('equipament/create_one/', EquipamentOneCreate.as_view(), name='create_one_equipament'),
    path('equipament/delete/<int:pk>/', EquipamentDelete.as_view(), name='delete_equipament'),
    path('accessory/list/<int:similar>/', AccessoryList.as_view(), name='list_accessory'),
    path('accessory/create/', AccessoryCreate.as_view(), name='create_accessory'),
    path('accessory/update_qtt/<int:pk>/', AccessoryQuantityUpdate.as_view(), name='acc_quantity'),
    path('accessory/delete/<int:pk>/', AccessoryDelete.as_view(), name='delete_accessory')
]