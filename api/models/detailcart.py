from django.db import models
from .product import Product
from .cart import Cart

class DetailCart(models.Model):
    cart     = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product  = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    price    = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total    = models.DecimalField(max_digits=10, decimal_places=2, default=0)