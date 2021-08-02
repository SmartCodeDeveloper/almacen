from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Brand, Category, Inventory, DetailInventory, Order, DetailOrder, Employee, Product, Unit, Cart, DetailCart, Movement, DetailMov, Manifest, DetailManifest


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model  = User
#         fields = ('id', 'first_name', 'last_name', 'email', )

class UserEditSerializer(serializers.ModelSerializer):
    class Meta:
        model  = User
        fields = ('is_active', )

class UserSimple2Serializer(serializers.ModelSerializer):
    class Meta:
        model  = User
        fields = ('email', 'password', 'is_active' )
        

class UserSimpleAppSerializer(serializers.ModelSerializer):
    class Meta:
        model  = User
        fields = ('username', 'password', 'is_active' )



class PasswordSerializer(serializers.Serializer):
    password  = serializers.CharField(max_length=50)


# class ClientAppSerializer(serializers.ModelSerializer):
#     user = UserSimpleAppSerializer()
#     class Meta:
#         model  = Client
#         fields = ('id', 'user', 'phone', 'name', 'device' )

# class EmployeeEditSerializer(serializers.ModelSerializer):
#     class Meta:
#         model  = Employee
#         fields = ('id', 'user', 'photo', 'name', 'lastname', 'address', 'information', )

class EmployeeEditSerializer(serializers.ModelSerializer):
    user = UserEditSerializer()
    class Meta:
        model  = Employee
        fields = ('id', 'user', 'photo', 'code', 'name', 'lastname', 'address', 'information', )


class EmployeeSerializer(serializers.ModelSerializer):
    user = UserSimple2Serializer()
    class Meta:
        model  = Employee
        fields = ('id', 'user', 'photo', 'code', 'name', 'lastname', 'address', 'information', )

class EmployeeShortSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Employee
        fields = ('id', 'information', 'code', 'name', 'lastname', 'address', )


class EmployeeReadSerializer(serializers.ModelSerializer):
    user = UserSimple2Serializer()
    photo = serializers.SerializerMethodField()
    
    class Meta:
        model  = Employee
        fields = ('id', 'user', 'photo', 'code', 'name', 'lastname', 'address', 'information' )
        
    def get_photo(self, employee):
        request = self.context.get('request')
        if employee.photo:
            photo_url = employee.photo.url
            return request.build_absolute_uri(photo_url)
        return request.build_absolute_uri("employees/Captura_de_Pantalla_2020-07-29_a_las_12.25.36_p.m..png")


class BrandSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()
    
    class Meta:
        model  = Brand
        fields = ('id', 'name', 'description', 'photo', 'active', )
    
    def get_photo(self, brand):
        request = self.context.get('request')
        print(brand)
        if brand.photo:
            print("llegando")
            print(brand)
            photo_url = brand.photo.url
            return request.build_absolute_uri(photo_url)
        return request.build_absolute_uri("brands/Captura_de_Pantalla_2020-07-29_a_las_12.25.36_p.m..png")
 

class BrandSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Brand
        fields = ('id', 'name', 'description', 'photo', 'active', )
               
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category 
        fields = ('id', 'parent', 'code', 'name', 'active', )

class Category2Serializer(serializers.ModelSerializer):
    class Meta:
        model  = Category 
        fields = ('id', 'name' )


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Cart
        fields = ('id', 'employee', 'date_created', 'date_updated', )


class CartDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model  = DetailCart
        fields = ('id', 'cart', 'product', 'quantity', 'price', 'total')

class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit 
        fields = ('id', 'name', )

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order 
        fields = ('id', 'employee', 'priority', 'status', 'date_delivery', 'torder', 'tpayment', 'description', )

class Order2Serializer(serializers.ModelSerializer):
    class Meta:
        model = Order 
        fields = ('id', 'employee', 'priority', 'status', 'date_delivery', 'date_delivery2', 'hour_delivery', 'torder', 'description', )

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order 
        fields = ('id', 'employee',)

class DetailOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetailOrder
        fields = ('id', 'order', 'product', 'quantity', 'price', 'total' )
        

class DetailCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetailOrder
        fields = ('id', 'cart', 'product', 'quantity', 'price', 'total' )

class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ('id', 'order', 'typemov', )


class DetailInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DetailInventory
        fields = ('id', 'inventory', 'product', 'quantity', 'price', 'total', )

class ProductSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'code', 'serie' , 'series', 'price', 'brand', 'unit', 'photo', 'active', 'stock', 'minstock', 'minstockclient', )

class ProductSerializer(serializers.ModelSerializer):
    photo      = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ('id', 'name', 'code', 'serie' , 'series', 'price', 'brand', 'unit', 'photo', 'active', 'stock', 'minstock', 'minstockclient', )
        
    def get_photo(self, product):
        request = self.context.get('request')
        if product.photo:
            photo_url = product.photo.url
            return request.build_absolute_uri(photo_url)
        return request.build_absolute_uri("products/Captura_de_Pantalla_2020-07-29_a_las_12.25.36_p.m..png")


class ProductFullSerializer(serializers.ModelSerializer):
    photo      = serializers.SerializerMethodField()
    categories = CategorySerializer(many=True)
    brand      = BrandSerializer()
    unit       = UnitSerializer()
    class Meta:
        model = Product
        fields = ('id', 'name', 'code', 'serie' , 'series', 'price', 'brand', 'unit', 'photo', 'active', 'categories', 'stock', 'minstock', 'minstockclient', )
        
    def get_photo(self, product):
        request = self.context.get('request')
        if product.photo:
            photo_url = product.photo.url
            return request.build_absolute_uri(photo_url)
        return request.build_absolute_uri("products/Captura_de_Pantalla_2020-07-29_a_las_12.25.36_p.m..png")


class CartDetailFullSerializer(serializers.ModelSerializer):
    product = ProductFullSerializer()
    class Meta:
        model  = DetailCart
        fields = ('id', 'cart', 'product', 'quantity', 'price', 'total')


class DetailOrderFullSerializer(serializers.ModelSerializer):
    product= ProductFullSerializer()
    class Meta:
        model = DetailOrder
        fields = ('id', 'order', 'product', 'quantity', 'price', 'total' )



class OrderFullSerializer(serializers.ModelSerializer):
    odetails = DetailOrderFullSerializer(many=True)
    class Meta:
        model = Order 
        fields = ('id', 'employee', 'priority', 'status', 'date_delivery', 'date_delivery2', 'hour_delivery',  'torder', 'description', 'date_created' ,'odetails' )


class MovementClientSerializer(serializers.ModelSerializer):
    class Meta:
        model   = Movement
        fields  = ('id','client', 'sign', 'typemov',)


class DetailInventorySerializer(serializers.ModelSerializer):
    product = ProductFullSerializer()
    class Meta:
        model   = DetailInventory
        fields  = ('id', 'inventory', 'product', 'quantity')


class DetailCreateSerializer(serializers.ModelSerializer):
    product = ProductFullSerializer()
    class Meta:
        model   = DetailMov
        fields  = ('id', 'product', 'quantity')

class MovementSerializer(serializers.ModelSerializer):
    sign      = serializers.SerializerMethodField()
    class Meta:
        model   = Movement
        fields  = ('id','client', 'sign', 'typemov', 'datemov', 'status', )
    
    def get_sign(self, mov):
        request = self.context.get('request')
        if mov.sign:
            sign_url = mov.sign.url
            return request.build_absolute_uri(sign_url)
        return request.build_absolute_uri("signs/Captura_de_Pantalla_2020-07-29_a_las_12.25.36_p.m..png")

class Movement2Serializer(serializers.ModelSerializer):
    sign         = serializers.SerializerMethodField()
    fromemployee = EmployeeShortSerializer()
    class Meta:
        model   = Movement
        fields  = ('id', 'fromemployee', 'client', 'sign', 'typemov', 'datemov', )
    
    def get_sign(self, mov):
        request = self.context.get('request')
        if mov.sign:
            sign_url = mov.sign.url
            return request.build_absolute_uri(sign_url)
        return request.build_absolute_uri("signs/Captura_de_Pantalla_2020-07-29_a_las_12.25.36_p.m..png")

class DetailMovementSerializer(serializers.ModelSerializer):
    product = ProductFullSerializer()
    class Meta:
        model   = DetailMov
        fields  = ('id', 'product', 'quantity', 'seriales',)

class ReportMovSerializer(serializers.Serializer):
    datefrom = serializers.DateField()
    dateto   = serializers.DateField()
    typemov  = serializers.IntegerField()
    employee = serializers.IntegerField()
    serie    = serializers.CharField()


class DetailManifestFullSerializer(serializers.ModelSerializer):
    product= ProductFullSerializer()
    class Meta:
        model = DetailManifest
        fields = ('id', 'order', 'product', 'quantity', )


class ManifestFullSerializer(serializers.ModelSerializer):
    omanifestdetails = DetailManifestFullSerializer(many=True)
    class Meta:
        model = Manifest 
        fields = ('id', 'employee', 'active', 'printer', 'date_manifest',  'description', 'omanifestdetails', 'receive', 'delivery' )

class ManifestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manifest 
        fields = ('id', 'employee', 'description', 'date_manifest', 'receive', 'delivery', 'order' )

class DetailManifestSerializer(serializers.ModelSerializer):
    class Meta:
        model  = DetailManifest
        fields = ('id', 'manifest', 'product', 'quantity', )