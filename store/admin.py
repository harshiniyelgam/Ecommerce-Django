from django.contrib import admin
from .models import product,Variations

# Register your models here.
class productadmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('product_name',)}
    list_display=('product_name','stock','Modified_date','is_avaliable')

class variationsadmin(admin.ModelAdmin):
    list_display=('product','variation_category','variation_value','is_active')
    list_editable=('is_active',)
    list_filter=('product','variation_category','variation_value')

admin.site.register(product,productadmin)
admin.site.register(Variations,variationsadmin)
