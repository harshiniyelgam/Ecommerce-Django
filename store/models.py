from django.db import models
from category.models import Category
from django.urls import reverse
class product(models.Model):
    product_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=255, blank=True)
    price=models.IntegerField()
    images = models.ImageField(upload_to='photos_products/', blank=True)
    stock=models.IntegerField()
    is_avaliable=models.BooleanField(default=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,null=True,blank=True)
    created_date=models.DateTimeField(auto_now_add=True)
    Modified_date=models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse('product_detail',args=[self.category.slug, self.slug])
    
    def __str__(self):
        return self.product_name