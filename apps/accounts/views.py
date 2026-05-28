from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import DetailView

from .forms import MasterProfileForm, RegistrationForm
from .models import MasterProfile


class MarketplaceLoginView(LoginView):
    template_name = "accounts/login.html"
    redirect_authenticated_user = True


class MarketplaceLogoutView(LogoutView):
    next_page = reverse_lazy("catalog:product_list")


def register(request):
    if request.user.is_authenticated:
        return redirect("catalog:product_list")
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Реєстрацію виконано. Ласкаво просимо!")
            return redirect("catalog:product_list")
    else:
        form = RegistrationForm()
    return render(request, "accounts/register.html", {"form": form})


@login_required
def profile(request):
    master = MasterProfile.objects.filter(user=request.user).first()
    return render(request, "accounts/profile.html", {"master": master})


@login_required
def become_master(request):
    if hasattr(request.user, "master_profile"):
        return redirect("accounts:profile_edit")
    if request.method == "POST":
        form = MasterProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile_obj = form.save(commit=False)
            profile_obj.user = request.user
            profile_obj.save()
            messages.success(request, "Профіль майстра створено.")
            return redirect("accounts:profile")
    else:
        form = MasterProfileForm()
    return render(request, "accounts/profile_edit.html", {"form": form, "creating": True})


@login_required
def profile_edit(request):
    master = get_object_or_404(MasterProfile, user=request.user)
    if request.method == "POST":
        form = MasterProfileForm(request.POST, request.FILES, instance=master)
        if form.is_valid():
            form.save()
            messages.success(request, "Профіль оновлено.")
            return redirect("accounts:profile")
    else:
        form = MasterProfileForm(instance=master)
    return render(request, "accounts/profile_edit.html", {"form": form, "creating": False})


class MasterDetailView(DetailView):
    model = MasterProfile
    template_name = "accounts/master_detail.html"
    context_object_name = "master"

    def get_context_data(self, **kwargs):
        from apps.catalog.models import Product
        from apps.reviews.models import Review

        ctx = super().get_context_data(**kwargs)
        ctx["products"] = Product.objects.filter(owner=self.object, is_active=True)
        ctx["reviews"] = Review.objects.filter(seller=self.object).select_related("author")
        return ctx
