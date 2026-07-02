from django.contrib import admin
from .models import product,Variations,ReviewRating,ProductGallery
import admin_thumbnails

# Register your models here.
@admin_thumbnails.thumbnail('image')
class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra=1

class productadmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('product_name',)}
    list_display=('product_name','stock','Modified_date','is_avaliable')
    inlines=[ProductGalleryInline]

class variationsadmin(admin.ModelAdmin):
    list_display=('product','variation_category','variation_value','is_active')
    list_editable=('is_active',)
    list_filter=('product','variation_category','variation_value')


class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra=1


admin.site.register(product,productadmin)
admin.site.register(Variations,variationsadmin)
admin.site.register(ReviewRating)
admin.site.register( ProductGallery)
