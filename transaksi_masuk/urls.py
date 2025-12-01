from django.urls import path
from .views import masuk_list, masuk_add

urlpatterns = [
    path("", masuk_list, name="masuk_list"),
    path("add/", masuk_add, name="masuk_add"),
]
