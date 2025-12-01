from django.urls import path
from .views import keluar_list, keluar_add

urlpatterns = [
    path("", keluar_list, name="keluar_list"),
    path("add/", keluar_add, name="keluar_add"),
]
