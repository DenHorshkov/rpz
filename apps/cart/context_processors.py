from .cart import Cart


def cart_summary(request):
    cart = Cart(request)
    return {"cart_summary": {"count": cart.count}}
