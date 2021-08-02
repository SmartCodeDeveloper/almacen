from django.db import models
from .category import Category
from .brand import Brand
from .unit  import Unit


class Product(models.Model):
    name     = models.CharField(max_length=100)
    code     = models.CharField(max_length=100)
    price    = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    serie    = models.CharField(max_length=100, null=True, blank=True)
    #category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    categories = models.ManyToManyField(Category)
    brand    = models.ForeignKey(Brand, null=True, on_delete=models.SET_NULL)
    unit     = models.ForeignKey(Unit, null=True, on_delete=models.SET_NULL)
    photo    = models.ImageField(upload_to="products", null=True, blank=True)
    stock    = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    minstock = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    minstockclient = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    series         = models.TextField(null=True, blank=True)
    series2        = models.TextField(null=True, blank=True)
    active         = models.BooleanField(default=True)