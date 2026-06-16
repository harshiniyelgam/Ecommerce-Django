from django.contrib import admin
from .models import product

# Register your models here.
class productadmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('product_name',)}
    list_display=('product_name','stock','Modified_date','is_avaliable')
admin.site.register(product,productadmin)
