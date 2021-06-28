from django.contrib import admin

# Register your models here.
from products.models import Category, Product, Like, Favorite, Bag

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Like)
admin.site.register(Favorite)
admin.site.register(Bag)

