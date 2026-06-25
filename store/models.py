from django.db import models
from category.models import Category
from django.urls import reverse

class product(models.Model):
    product_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=255, blank=True)
    price = models.IntegerField()
    images = models.ImageField(upload_to='photos_products/', blank=True)
    stock = models.IntegerField()
    is_avaliable = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    Modified_date = models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.product_name
class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager,self).filter(variation_category='color',is_active=True)
    def sizes(self):
        return super(VariationManager,self).filter(variation_category='size',is_active=True)
    

varitaion_category_choice=(
    ('color','color'),
    ('size','size'),
)        
class Variations(models.Model):
    product=models.ForeignKey(product,on_delete=models.CASCADE)
    variation_category=models.CharField(max_length=100,choices=varitaion_category_choice)
    variation_value=models.CharField(max_length=100)
    is_active=models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    objects=VariationManager()


    def __str__(self):
        return self.variation_value 