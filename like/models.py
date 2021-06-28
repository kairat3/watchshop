from django.db import models

from products.models import Product


class Like(models.Model):
    owner = models.ForeignKey("user.CustomUser", on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='likes')
    like = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.owner}-->{self.post}'
