from django.contrib import admin
from .models import Brand, Category, Employee, Product, Unit, Order, DetailOrder, Cart, DetailCart, Inventory, DetailInventory, Movement, Manifest, DetailMov

# Register your models here.

class BrandAdmin(admin.ModelAdmin):
    pass

class CategoryAdmin(admin.ModelAdmin):
    pass

class EmployeeAdmin(admin.ModelAdmin):
    pass

class ProductAdmin(admin.ModelAdmin):
    pass

class UnitAdmin(admin.ModelAdmin):
    pass

class OrderAdmin(admin.ModelAdmin):
    pass

class DetailOrderAdmin(admin.ModelAdmin):
    pass

class InventoryAdmin(admin.ModelAdmin):
    pass

class DetailInventoryAdmin(admin.ModelAdmin):
    pass

class MovementAdmin(admin.ModelAdmin):
    pass

class ManifestAdmin(admin.ModelAdmin):
    pass

class DetailMovAdmin(admin.ModelAdmin):
    pass


admin.site.register(Brand, BrandAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Unit, UnitAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(DetailOrder, DetailOrderAdmin)
admin.site.register(Inventory, InventoryAdmin)
admin.site.register(DetailInventory, DetailInventoryAdmin)
admin.site.register(Movement, MovementAdmin)
admin.site.register(Manifest, ManifestAdmin)
admin.site.register(DetailMov, DetailMovAdmin)