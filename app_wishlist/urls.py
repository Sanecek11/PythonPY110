from django.urls import path
from .views import *


app_name = 'app_wishlist'

urlpatterns = [
    path('wishlist/', wishlist_view, name="wishlist_view"),
    path('wishlist/api/add/<str:id_product>', wishlist_add_json, name='wishlist_add'),
    path('wishlist/api/del/<str:id_product>', wishlist_del_json, name='wishlist_del'),
    path('wishlist/api/', wishlist_json, name='wishlist_json'),
    path('wishlist/remove/<str:id_product>', wishlist_remove_view, name="remove"),
]
