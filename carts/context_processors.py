from .models import Cart, CardItem
from .views import _cart_id

def counter(request):
    cart_count = 0

    print("Counter called")

    if 'admin' in request.path:
        return {}

    if request.user.is_authenticated:
        cart_items = CardItem.objects.filter(user=request.user)
    else:
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CardItem.objects.filter(cart=cart)
        except Cart.DoesNotExist:
            cart_items = []

    print("Items:", cart_items)

    for item in cart_items:
        print(item.id, item.quantity)
        cart_count += item.quantity

    print("Cart Count =", cart_count)

    return {'cart_count': cart_count}