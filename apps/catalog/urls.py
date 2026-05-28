from django.urls import path

from . import views

app_name = "catalog"

urlpatterns = [
    path("", views.ProductListView.as_view(), name="product_list"),
    path("products/new/", views.product_create, name="product_create"),
    path("products/my/", views.my_products, name="my_products"),
    path("products/<slug:slug>/", views.ProductDetailView.as_view(), name="product_detail"),
    path("products/<slug:slug>/edit/", views.ProductUpdateView.as_view(), name="product_edit"),
    path("products/<slug:slug>/delete/", views.product_delete, name="product_delete"),
]
