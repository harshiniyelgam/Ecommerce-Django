from django.shortcuts import render, get_object_or_404
from .models import product
from category.models import Category
from carts.models import CardItem
from carts.views import _cart_id
from django.http import HttpResponse
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from django.db.models import Q

def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug is not None:
        categories = None
        products = None
        categories = get_object_or_404(Category, slug=category_slug)

        products = product.objects.filter(category=categories,is_avaliable=True).order_by('id')
        paginator = Paginator(products, 1)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()

    else:
        products = product.objects.filter(is_avaliable=True)
        paginator = Paginator(products,3)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)


        product_count = products.count()

    context = {
        'products': paged_products,
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
    in_cart = CardItem.objects.filter(cart__cart_id=_cart_id(request), Product=single_product).exists()
    
    context = {
        'single_product': single_product,
        'in_cart':in_cart,
    }

    return render(request, 'store/products_details.html', context)
def search(request):
    if 'keyword' in request.GET:
        keyword=request.GET['keyword']
        if keyword:
            products = product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) |Q(product_name__icontains=keyword))           
            product_count = products.count()
            context={
                'products':products,
                'product_count':product_count,

            }

    return render(request, 'store/store.html',context)