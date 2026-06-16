from django.contrib import admin
from .models import Category
# Register your models here.
class Category_admin(admin.ModelAdmin):
    prepopulated_fields={'slug':('category_name',)}
    list_display=('category_name','slug')
admin.site.register(Category,Category_admin)
