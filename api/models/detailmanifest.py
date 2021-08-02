from django.db import models
from .manifest import Manifest
from .product import Product

class DetailManifest(models.Model):
    manifest  = models.ForeignKey(Manifest, on_delete=models.CASCADE, related_name='omanifestdetails') 
    product   = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity  = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    seriales  = models.TextField(null=True, blank=True)