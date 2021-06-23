import os
import random
from ckeditor.fields import RichTextField
from django.db import models


class DataABC(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(DataABC):
    name = models.CharField(max_length=150)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return f'{self.name}-->'


class Product(DataABC):
    category = models.ForeignKey(Category, related_name='category', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    quantity = models.PositiveIntegerField(default=0)
    available = models.BooleanField(default=False)
    preview = models.ImageField(upload_to='images/', blank=True)

    def __str__(self):
        return f"{self.category}-->{self.title}"


class PostImages(models.Model):
    title = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='images/')
    post = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')

    class Meta:
        verbose_name = 'image'
        verbose_name_plural = 'images'

    @staticmethod
    def generate_name():
        import random
        return "Image" + str(random.randint(1, 99999))

    def save(self, *args, **kwargs):
        self.title = self.generate_name()
        return super(PostImages, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} --> {self.post.id}"
