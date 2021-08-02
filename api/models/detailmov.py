from django.db import models
from .movement import Movement
from .product  import Product


class DetailMov(models.Model):
    movement  = models.ForeignKey(Movement, on_delete=models.CASCADE)
    product   = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity  = models.DecimalField(max_digits=10, decimal_places=2)
    seriales  = models.TextField(null=True, blank=True)