from django.db import models
from .order import Order
from .product import Product

class DetailOrder(models.Model):
    order    = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='odetails')
    product  = models.ForeignKey(Product, on_delete=models.CASCADE)
    seriales = models.TextField(null=True, blank=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    price    = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total    = models.DecimalField(max_digits=10, decimal_places=2, default=0)