from django.db import models
from .inventory import Inventory
from .product import Product

class DetailInventory(models.Model):
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE) 
    product   = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity  = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    seriales  = models.TextField(null=True, blank=True)
    # price     = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    # total     = models.DecimalField(max_digits=10, decimal_places=2, default=0)