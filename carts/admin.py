from django.contrib import admin
from .models import Cart, CardItem


class CartAdmin(admin.ModelAdmin):
    list_display = ('cart_id','date_added')


class CardItemAdmin(admin.ModelAdmin):
    list_display = ('Product','user','cart','quantity', 'is_active')


admin.site.register(Cart, CartAdmin)
admin.site.register(CardItem, CardItemAdmin)