from django.contrib import admin
from django.urls import path

from catalog import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.products_list, name='products_list'),
    path('products/', views.products_list, name='products'),
    path('products', views.products_list),
    path('replenish/<int:count>/', views.replenish, name='replenish'),
    path('replenish/<int:count>', views.replenish),
]
