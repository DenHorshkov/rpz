from django.urls import path

from . import views

app_name = "reviews"

urlpatterns = [
    path("master/<int:master_id>/new/", views.create, name="create"),
]
