from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('mas-pedidos', views.report_bestseller , name="bestseller"),
    path('bajo-stock', views.reportlowstock, name="lowstock"),
    path('manifiestos', views.listmanifest, name="list_manifiests"),
    path('manifiesto', views.manifest, name="manifiest"),
    path('manifiesto/<int:manifest>', views.showmanifest, name="show_manifiest"),
    path('manifiesto-orden/<int:order>', views.manifestorder, name="manifiestorder"),
    path('productos', views.product, name="products"),
    path('productos-categoria/<int:category>', views.product_category, name="products_category"),
    path('marcas', views.brand, name="brands"),
    path('categorias/<int:category>', views.category, name="categories"),
    path('empleados', views.employee, name="employees"),
    path('orden', views.order, name="order"),
    path('orden/<int:order>', views.orderEdit, name="order_edit"),
    path('ordenes', views.listorder, name="orders"),
    path('reporte-inventario', views.report_inventory, name="report_inventory"),
    path('reporte-movimientos', views.report_mov, name="report_mov"),
    path('reporte-principal', views.report_inventory_principal, name="report_principal"),
    path('reporte-principal-filter', views.report_inventory_principal_filter, name="report_principal_filter"),
    path('reporte-principal-excel', views.report_excel_stock_principal, name="report_principal_excel"),
    path('reporte-bajo-stock-excel', views.report_excel_low_stock, name="report_low_stock_excel"),
    path('reporte-mas-vendidos-excel', views.report_excel_best_seller, name="report_best_seller_excel"),
    path('notificaciones', views.listnotificaciones, name="notifications"),
    path('run-notificaciones', views.notificaciones),
    path('transferencias', views.listtransfer, name="transferencias"),
    path('csv', views.load_csv, name="csv_load"),
    
]