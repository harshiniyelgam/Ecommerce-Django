from django.shortcuts import render, get_object_or_404
from .models import product
from category.models import Category

def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug is not None:
        categories = get_object_or_404(Category, slug=category_slug)

        products = product.objects.filter(
            category=categories,
            is_avaliable=True
        )

        product_count = products.count()

    else:
        products = product.objects.filter(
            is_avaliable=True
        )

        product_count = products.count()

    context = {
        'products': products,
        'product_count': product_count,
    }

    return render(request, 'store/store.html', context)

from django.shortcuts import render, get_object_or_404
from .models import product


def products_details(request, category_slug, product_slug):
    single_product = get_object_or_404(
        product,
        category__slug=category_slug,
        slug=product_slug
    )

    context = {
        'single_product': single_product,
    }

    return render(request, 'store/products_details.html', context)