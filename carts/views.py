from django.shortcuts import render, redirect, get_object_or_404
from store.models import product,Variations
from .models import Cart, CardItem
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required



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

    cart, created = Cart.objects.get_or_create(
        cart_id=_cart_id(request)
    )

    if request.user.is_authenticated:
        cart_items = CardItem.objects.filter(
            Product=Product,
            user=request.user
        )
    else:
        cart_items = CardItem.objects.filter(
            Product=Product,
            cart=cart
        )

    is_cart_item_exists = cart_items.exists()

    if is_cart_item_exists:

        ex_var_list = []
        ids = []

        for item in cart_items:
            existing_variation = list(item.variations.all())
            ex_var_list.append(existing_variation)
            ids.append(item.id)

        if product_variation in ex_var_list:
            index = ex_var_list.index(product_variation)
            item_id = ids[index]

            cart_item = CardItem.objects.get(id=item_id)
            cart_item.quantity += 1
            cart_item.save()

        else:
            if request.user.is_authenticated:
                cart_item = CardItem.objects.create(
                    Product=Product,
                    quantity=1,
                    user=request.user
                )
            else:
                cart_item = CardItem.objects.create(
                    Product=Product,
                    quantity=1,
                    cart=cart
                )

            if product_variation:
                cart_item.variations.add(*product_variation)

    else:
        if request.user.is_authenticated:
            cart_item = CardItem.objects.create(
                Product=Product,
                quantity=1,
                user=request.user
            )
        else:
            cart_item = CardItem.objects.create(
                Product=Product,
                quantity=1,
                cart=cart
            )

        if product_variation:
            cart_item.variations.add(*product_variation)

    return redirect('cart')


def remove_cart(request, product_id, cart_item_id):
    Product = get_object_or_404(product, id=product_id)

    try:
        if request.user.is_authenticated:
            cart_item = get_object_or_404(
                CardItem,
                Product=Product,
                user=request.user,
                id=cart_item_id
            )
        else:
            cart = get_object_or_404(Cart, cart_id=_cart_id(request))
            cart_item = get_object_or_404(
                CardItem,
                Product=Product,
                cart=cart,
                id=cart_item_id
            )

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()

    except:
        pass

    return redirect('cart')
def remove_cart_item(request, product_id, cart_item_id):
    Product = get_object_or_404(product, id=product_id)

    if request.user.is_authenticated:
        cart_item = get_object_or_404(
            CardItem,
            Product=Product,
            user=request.user,
            id=cart_item_id
        )
    else:
        cart = get_object_or_404(Cart, cart_id=_cart_id(request))
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
        tax = 0
        grand_total = 0

        if request.user.is_authenticated:
            cart_items = CardItem.objects.filter(
                user=request.user,
                is_active=True
            )
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CardItem.objects.filter(
                cart=cart,
                is_active=True
            )

        for cart_item in cart_items:
            total += cart_item.Product.price * cart_item.quantity
            quantity += cart_item.quantity

        tax = (2 * total) / 100
        grand_total = total + tax

    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }

    return render(request, 'store/cart.html', context)

@login_required(login_url='login')
def checkout(request,total=0, quantity=0, cart_items=None):
    try:
        if request.user.is_authenticated:
            cart_items = CardItem.objects.filter(
                user=request.user,
                is_active=True
            )
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
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


    return render(request,'store/checkout.html',context)