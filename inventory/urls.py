from django.urls import path
from . import views

urlpatterns = [
    path("", views.barang_list, name="barang_list"),
    path("add/", views.barang_add, name="barang_add"),
    path("edit/<int:id_barang>/", views.barang_edit, name="barang_edit"),
    path("delete/<int:id_barang>/", views.barang_delete, name="barang_delete"),
]
