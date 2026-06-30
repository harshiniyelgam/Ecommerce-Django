from django.shortcuts import render, get_object_or_404
from .models import product
from category.models import Category
from carts.models import CardItem
from carts.views import _cart_id
from django.http import HttpResponse
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import redirect
from .models import ReviewRating
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required
from orders.models import OrderProduct

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
from .models import product, ReviewRating
from carts.models import CardItem
from carts.views import _cart_id
from orders.models import OrderProduct

def products_details(request, category_slug, product_slug):

    single_product = get_object_or_404(
        product,
        category__slug=category_slug,
        slug=product_slug
    )

    # Check if product is already in cart
    if request.user.is_authenticated:
        in_cart = CardItem.objects.filter(
            user=request.user,
            Product=single_product      # Use product=single_product if your field name is product
        ).exists()
    else:
        in_cart = CardItem.objects.filter(
            cart__cart_id=_cart_id(request),
            Product=single_product
        ).exists()

    # Check if the user has purchased this product
    if request.user.is_authenticated:
        orderproduct = OrderProduct.objects.filter(
            user=request.user,
            product=single_product,
            ordered=True
        ).exists()
    else:
        orderproduct = False

    # Fetch approved reviews
    reviews = ReviewRating.objects.filter(
        product=single_product,
        status=True
    ).order_by('-created_at')

    context = {
        'single_product': single_product,
        'in_cart': in_cart,
        'orderproduct': orderproduct,
        'reviews': reviews,
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



@login_required(login_url='login')
def submit_review(request, product_id):

    url = request.META.get('HTTP_REFERER')

    if request.method == 'POST':

        try:
            review = ReviewRating.objects.get(
                user=request.user,
                product_id=product_id
            )

            form = ReviewForm(request.POST, instance=review)

            if form.is_valid():
                form.save()
                messages.success(request,
                                 'Thank you! Your review has been updated.')

        except ReviewRating.DoesNotExist:

            form = ReviewForm(request.POST)

            if form.is_valid():

                data = ReviewRating()

                data.subject = form.cleaned_data['subject']
                data.review = form.cleaned_data['review']
                data.rating = form.cleaned_data['rating']
                data.ip = request.META.get('REMOTE_ADDR')

                data.product_id = product_id
                data.user = request.user

                data.save()

                messages.success(request,
                                 'Thank you! Your review has been submitted.')

            else:
                print(form.errors)

    return redirect(url)