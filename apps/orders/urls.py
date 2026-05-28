from django.urls import path

from . import views

app_name = "orders"

urlpatterns = [
    path("checkout/", views.checkout, name="checkout"),
    path("my/", views.my_orders, name="my_orders"),
    path("<int:pk>/", views.detail, name="detail"),
    path("<int:pk>/pay/", views.pay, name="pay"),
]
