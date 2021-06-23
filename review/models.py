from django.db import models

from products.models import Product


class Review(models.Model):
    owner = models.ForeignKey('user.CustomUser', related_name='review', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='review', on_delete=models.CASCADE)
    body = models.TextField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.owner}-->{self.product}"
