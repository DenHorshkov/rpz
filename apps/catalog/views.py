from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, UpdateView

from .forms import ProductForm, ProductImageForm
from .models import Category, Product, ProductImage


class ProductListView(ListView):
    model = Product
    template_name = "catalog/product_list.html"
    context_object_name = "products"
    paginate_by = 12

    def get_queryset(self):
        qs = Product.objects.filter(is_active=True).select_related("owner", "category")
        category_slug = self.request.GET.get("category")
        search = self.request.GET.get("q")
        if category_slug:
            qs = qs.filter(category__slug=category_slug)
        if search:
            qs = qs.filter(title__icontains=search)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["categories"] = Category.objects.all()
        ctx["selected_category"] = self.request.GET.get("category", "")
        ctx["search_query"] = self.request.GET.get("q", "")
        return ctx


class ProductDetailView(DetailView):
    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"

    def get_queryset(self):
        return Product.objects.select_related("owner", "category").prefetch_related("images")


class SellerRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self) -> bool:
        return self.request.user.is_authenticated and self.request.user.is_seller


class OwnerRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self) -> bool:
        product = self.get_object()
        return product.owner.user_id == self.request.user.id


@login_required
def product_create(request):
    if not request.user.is_seller:
        messages.warning(request, "Спершу створіть профіль майстра.")
        return redirect("accounts:become_master")
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.owner = request.user.master_profile
            product.save()
            for f in request.FILES.getlist("images"):
                ProductImage.objects.create(product=product, image=f)
            messages.success(request, "Товар створено.")
            return redirect(product.get_absolute_url())
    else:
        form = ProductForm()
    return render(request, "catalog/product_form.html", {"form": form, "creating": True})


class ProductUpdateView(OwnerRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"

    def get_success_url(self):
        return self.object.get_absolute_url()

    def form_valid(self, form):
        response = super().form_valid(form)
        for f in self.request.FILES.getlist("images"):
            ProductImage.objects.create(product=self.object, image=f)
        messages.success(self.request, "Товар оновлено.")
        return response


@login_required
def product_delete(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if product.owner.user_id != request.user.id:
        return redirect("catalog:product_list")
    if request.method == "POST":
        product.delete()
        messages.info(request, "Товар видалено.")
        return redirect("catalog:my_products")
    return render(request, "catalog/product_confirm_delete.html", {"product": product})


@login_required
def my_products(request):
    if not request.user.is_seller:
        return redirect("accounts:become_master")
    products = Product.objects.filter(owner=request.user.master_profile)
    return render(request, "catalog/my_products.html", {"products": products})
