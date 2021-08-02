from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token
from .views.brand import BrandList, BrandDetail, OrderListBrandJson, brandJson, brandAll
from .views.employee import EmployeeList, EmployeeDetail, OrderListEmployeeJson, profileEmployee, change_password_login, changeProfileEmployee, avatar, employeeJson, getAllEmployee
from .views.category import CategoryList, CategoryDetail, OrderListCategoryJson, categoryJson, categoryAll
from .views.product import ProductList, ProductDetail, OrderListProductJson, associateProductCategory, listProductAll, searchProductAll, searchProductFull, productSerialJson
from .views.cart import getCart, addDetailCart, removeDetailCart, processCart, restDetailCart
from .views.order import OrderList, OrderDetail, OrderListOrdenJson, changeOrder, removeDetail, ordersEmployee
from .views.inventory import InventoryList, InventoryDetail, inventory_employee,inventory_employee_report
from .views.unit import UnitList, UnitDetail
from .views.movement import create_movement, my_movement, detail_mov, create_transference, detail_mov_report, OrderListTransferJson, get_transfer, changeTransference
from .views.manifest import ManifestList, ManifestDetail, OrderListManifestJson, changeManifest
from .views.notification import OrderListNotificationJson

urlpatterns = [
    path('api-token-auth/', obtain_jwt_token),
    path('brand', BrandList.as_view()),
    path('brand/<int:pk>', BrandDetail.as_view()),
    path('all-employee', getAllEmployee),
    path('employee', EmployeeList.as_view()),
    path('employee/<int:pk>', EmployeeDetail.as_view()),
    path('category', CategoryList.as_view() ),
    path('category/<int:pk>', CategoryDetail.as_view()),
    path('product', ProductList.as_view()),
    path('product/<int:pk>', ProductDetail.as_view()),
    # path('cart', CartList.as_view()),
    # path('cart/<int:pk>', CartDetail.as_view()),
    path('order', OrderList.as_view()),
    path('order/<int:pk>', OrderDetail.as_view()),
    path('order-change/<int:order>', changeOrder),
    path('detail-order/<int:pk>', removeDetail),
    path('manifest', ManifestList.as_view()),
    path('manifest/<int:pk>', ManifestDetail.as_view()),
    path('manifest-change/<int:manifest>', changeManifest),
    path('inventory', InventoryList.as_view()),
    path('inventory/<int:pk>', InventoryDetail.as_view()),
    path('unit', UnitList.as_view()),
    path('unit/<int:pk>', UnitDetail.as_view()),
    path('list-brand', OrderListBrandJson.as_view(), name='order_list_brand_json'),
    path('list-category', OrderListCategoryJson.as_view(), name='order_list_category_json'),
    path('list-employee', OrderListEmployeeJson.as_view(), name='order_list_employee_json'),
    path('list-product', OrderListProductJson.as_view(), name='order_list_product_json'),
    path('list-products-all', listProductAll, name='list_product_all'),
    path('search-product-all/<str:search>', searchProductAll, name='search_product_all'),
    path('list-order', OrderListOrdenJson.as_view(), name='order_list_orden_json'),
    path('list-product-serial/<int:pk>', productSerialJson, name="product_serial_json"),
    path('list-tranfer', OrderListTransferJson.as_view(), name='order_list_transfer_json'),
    path('list-manifest', OrderListManifestJson.as_view(), name='order_list_manifest_json'),
    path('list-notification', OrderListNotificationJson.as_view(), name="order_list_notification_json"),
    path('list-employee-json', employeeJson, name="list_employee_json"),
    path('list-brand-json', brandJson,name="list_brand_json"),
    path('list-category-json', categoryJson ,name="list_category_json"),
    path('assoc-product-category/<int:pk>', associateProductCategory, name="associate_product_category"),
    path('perfil-empleado', profileEmployee, name="profile_employee"),
    path('change-password-login/', change_password_login),
    path('cambiar-perfil-empleado', changeProfileEmployee),
    path('avatar', avatar),
    path('cart', getCart, name="cart"),
    path('add-cart', addDetailCart, name="add_cart"),
    path('rest-cart', restDetailCart, name="rest_cart"),
    path('remove-cart/<int:pk>', removeDetailCart, name="remove_cart"),
    path('process-cart/<int:tpayment>', processCart, name="process_cart"),
    path('order-employee', ordersEmployee, name="order_employee"),
    path('movement-create', create_movement, name="create_movement"),
    path('inventory-employee', inventory_employee, name="inventory_employee"),
    path('inventory-employee/<int:employee>', inventory_employee_report, name="inventory_employee_report"),
    path('my-movement/<int:typemov>', my_movement, name="my_movement"),
    path('detail-movement/<int:mov>', detail_mov, name="detail_mov"),
    path('movement-report', detail_mov_report, name="movement_report"),
    path('transference-create', create_transference, name="create_transference"),
    path('brand-all', brandAll, name="brand_all"),
    path('category-all', categoryAll, name="category_all"),
    path('search-product-full', searchProductFull, name="searchProductFull"),
    path('transference/<int:mov>', get_transfer, name="get_transfer"),
    path('change-transference/<int:mov>', changeTransference, name="changeTransference"),
]
