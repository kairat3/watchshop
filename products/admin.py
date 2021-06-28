from django.contrib import admin

# Register your models here.
from products.models import Category, Product, Like, Favorite

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Like)
admin.site.register(Favorite)
