from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("login/", views.MarketplaceLoginView.as_view(), name="login"),
    path("logout/", views.MarketplaceLogoutView.as_view(), name="logout"),
    path("register/", views.register, name="register"),
    path("profile/", views.profile, name="profile"),
    path("profile/edit/", views.profile_edit, name="profile_edit"),
    path("become-master/", views.become_master, name="become_master"),
    path("masters/<int:pk>/", views.MasterDetailView.as_view(), name="master_detail"),
]
