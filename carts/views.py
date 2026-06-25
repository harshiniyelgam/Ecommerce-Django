from django.shortcuts import render, redirect, get_object_or_404
from store.models import product,Variations
from .models import Cart, CardItem
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist



def _cart_id(request):
    cart = request.session.session_key

    if not cart:
        cart = request.session.create()

    return cart


def add_cart(request, product_id):
    Product = get_object_or_404(product, id=product_id)

    product_variation = []

    if request.method == 'POST':
        for item in request.POST:
            key = item
            value = request.POST[key]

            try:
                variation = Variations.objects.get(
                    product=Product,
                    variation_category__iexact=key,
                    variation_value__iexact=value
                )
                product_variation.append(variation)

            except Variations.DoesNotExist:
                pass

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id=_cart_id(request)
        )

    is_cart_item_exists = CardItem.objects.filter(
        Product=Product,
        cart=cart
    ).exists()

    if is_cart_item_exists:

        cart_items = CardItem.objects.filter(
            Product=Product,
            cart=cart
        )

        ex_var_list = []
        ids = []

        for item in cart_items:
            existing_variation = list(item.variations.all())
            ex_var_list.append(existing_variation)
            ids.append(item.id)

        if product_variation in ex_var_list:

            index = ex_var_list.index(product_variation)
            item_id = ids[index]

            cart_item = CardItem.objects.get(
                id=item_id
            )

            cart_item.quantity += 1
            cart_item.save()

        else:

            cart_item = CardItem.objects.create(
                Product=Product,
                quantity=1,
                cart=cart
            )

            if product_variation:
                cart_item.variations.add(*product_variation)

    else:

        cart_item = CardItem.objects.create(
            Product=Product,
            quantity=1,
            cart=cart
        )

        if product_variation:
            cart_item.variations.add(*product_variation)

    return redirect('cart')


def remove_cart(request, product_id,cart_item_id):
    Product = get_object_or_404(product, id=product_id)
    cart = get_object_or_404(
        Cart,
        cart_id=_cart_id(request)
    )
    try:
        cart_item = get_object_or_404(CardItem,Product=Product,cart=cart,id=cart_item_id)

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass        

    return redirect('cart')


def remove_cart_item(request, product_id,cart_item_id):
    Product = get_object_or_404(product, id=product_id)

    cart = get_object_or_404(
        Cart,
        cart_id=_cart_id(request)
    )

    cart_item = get_object_or_404(
        CardItem,
        Product=Product,
        cart=cart,
        id=cart_item_id
    )

    cart_item.delete()

    return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None):
    try:
        cart = Cart.objects.get(
            cart_id=_cart_id(request)
        )

        cart_items = CardItem.objects.filter(
            cart=cart,
            is_active=True
        )

        for cart_item in cart_items:
            total += (
                cart_item.Product.price *
                cart_item.quantity
            )
            quantity += cart_item.quantity

        tax = (2 * total) / 100
        grand_total = total + tax

    except ObjectDoesNotExist:
        cart_items = []
        tax = 0
        grand_total = 0

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }

    return render(request, 'store/cart.html', context)