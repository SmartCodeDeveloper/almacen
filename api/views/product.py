from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from ..models import Product, Category, Brand
from ..serializers import ProductSerializer, ProductFullSerializer, Category2Serializer, ProductSaveSerializer, BrandSerializer, CategorySerializer
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape
from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.parsers import MultiPartParser, FormParser

class ProductList(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAdminUser]
    
    def get(self, request, format=None):
        query = self.request.GET.get('query', None)
        
        if query:
            products      = Product.objects.filter(Q(code__istartswith=query)| Q(name__istartswith=query))
        else:
            products      = Product.objects.all()
            
        serializer    = ProductSerializer(products, many=True, context={"request": request})
        return Response(serializer.data)
    
    def post(self, request, format=None):
        print(request)
        serializer = ProductSaveSerializer(data=request.data, context={"request": request})
        
        if serializer.is_valid():
            print(serializer.validated_data)
            name     = serializer.validated_data["name"]
            code     = serializer.validated_data["code"]
            price    = serializer.validated_data["price"]
            #category = serializer.validated_data["category"]
            brand    = serializer.validated_data["brand"]
            unit     = serializer.validated_data["unit"]
            stock    = serializer.validated_data["stock"]
            active   = serializer.validated_data["active"]
            minstock = serializer.validated_data["minstock"]
            minstockclient = serializer.validated_data["minstockclient"]
            
            photo = None
            if "photo" in serializer.validated_data:
                photo = serializer.validated_data["photo"]
            
            serie = None
            if "serie" in serializer.validated_data:
                serie = serializer.validated_data["serie"]
                
            
            series = None 
            if "series" in serializer.validated_data:
                series = serializer.validated_data["series"]
            
                
            
            productFind = Product.objects.filter(code=code).first()
            
            if productFind is None:
                productNew = Product.objects.create(name=name, code=code, price=price, brand=brand, unit=unit, active=active, photo=photo, stock=stock, serie=serie, minstock=minstock, minstockclient=minstockclient, series=series)
                serializer = ProductSerializer(productNew, context={"request": request})
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response("codigo de producto existe", status=status.HTTP_406_NOT_ACCEPTABLE)
                
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductDetail(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAdminUser]
    
    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        product  = self.get_object(pk)
        serializer   = ProductFullSerializer(product, context={"request": request})
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        product       = self.get_object(pk)
        serializer    = ProductSaveSerializer(product, data=request.data)
        
        print(request.data)
        
        if serializer.is_valid():
            
            print(serializer.validated_data)
            
            name     = serializer.validated_data["name"]
            code     = serializer.validated_data["code"]
            price    = serializer.validated_data["price"]
            brand    = serializer.validated_data["brand"]
            unit     = serializer.validated_data["unit"]
            active   = serializer.validated_data["active"]
            stock    = serializer.validated_data["stock"]
            minstock = serializer.validated_data["minstock"]
            minstockclient = serializer.validated_data["minstockclient"]
            photo    = None
            serie    = None
            
            if "photo" in serializer.validated_data:
                photo = serializer.validated_data["photo"]
                
            
            if "serie" in serializer.validated_data:
                serie = serializer.validated_data["serie"]
                
                        
            series = None 
            if "series" in serializer.validated_data:
                series = serializer.validated_data["series"]
            
            product.name     = name
            product.code     = code
            product.price    = price
            product.stock    = stock
            product.brand    = brand
            product.unit     = unit 
            product.serie    = serie
            product.minstock = minstock
            product.minstockclient = minstockclient
            product.series   = series
            product.active   = active
            
            print("sdasdasdasda")
            print(photo)
            
            if photo is not None:
                product.photo = photo
            
            
            productFind = Product.objects.filter(code=code).first()
            
            if ((productFind is None) or (productFind==product)):
                product.save()
                serializer = ProductSerializer(product, context={"request": request})
                return Response(serializer.data)
            else:
                return Response("codigo de producto existe", status=status.HTTP_406_NOT_ACCEPTABLE)
                
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        product = self.get_object(pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderListProductJson(BaseDatatableView):
    order_columns = ['id',]

    def get_initial_queryset(self):
        return  Product.objects.all()

    def filter_queryset(self, qs):
        search    = self.request.GET.get('search[value]', None)
        category  = self.request.GET.get('categoryproduct', None)
        

        if(category):
            qs = qs.filter(categories__pk=category)

            
        if search:
            qs = qs.filter(Q(code__istartswith=search)| Q(name__istartswith=search)| Q(brand__name__istartswith=search))

        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            
            status = item.active 
            
            statusHtml = "Inactivo"
            
            if(status):
                statusHtml = "Activo"
            
            serie = ""
            if(item.serie):
                serie = item.serie
                
            brand = ""
            if(item.brand):
                brand = item.brand.name
            
            unitname = ""
            if(item.unit):
                unitname = item.unit.name
            
            
            catNames =  ""
            categories = item.categories.all()
            for category in categories:
                catNames = category.code+" "+category.name+", "

            
            json_data.append([
                escape("{0}".format(item.code)),
                escape("{0}".format(item.name)),
                escape("{0}".format(brand)),
                escape("{0}".format(serie)),
                escape("{0}".format(catNames)),
                escape("{0}".format(item.stock)),
                escape("{0}".format(unitname)),
                escape("{0}".format(item.price)),
                statusHtml,
                '<i data-id="{0}"  class="la la-pencil-square ico-edit js-edit"></i>'.format(item.id),
                '<i data-id="{0}"class="la la-trash ico-trash js-delete"></i>'.format(item.id),
            ])
            
        return json_data


@api_view(["GET"])
def listProductAll(request):
    # print(start)
    # to    = 5*start
    # froms =  to + 5
    brands     = Brand.objects.all()
    categories = Category.objects.filter(parent__isnull=True)
    products   = Product.objects.all()
    serializer = ProductFullSerializer(products, many=True, context={"request": request})
    serializerBrand = BrandSerializer(brands, many=True, context={"request": request}) 
    serializerCategory = CategorySerializer(categories, many=True) 
    
    return Response({"products": serializer.data, "brands": serializerBrand.data, "categories": serializerCategory.data })


@api_view(["GET"])
def searchProductAll(request, search):
    products   = Product.objects.filter(Q(code__istartswith=search)| Q(name__istartswith=search)| Q(brand__name__istartswith=search) | Q(categories__name__istartswith=search) | Q(categories__code__istartswith=search))
    serializer = ProductFullSerializer(products, many=True, context={"request": request})
    return Response({"products": serializer.data})


@api_view(["POST"])
def searchProductFull(request):
    data = request.data
    categories = data["categories"]
    brands     = data["brands"]
    search     = data["search"]
    
    print("===================")
    print(categories)
    print(brands)
    print(search)
    print("===================")
    
    
    idscat           = categories
    idsbrand         = brands
    idstotal         = []
    products         = []
    
    for idcat in idscat:
        category         = Category.objects.get(pk=idcat)
        resultcategories = findListCategory(category, [])
        if len(resultcategories)>0:
            idstotal = list(set(idstotal).union(resultcategories))
    
    
    if search is None:
        search = ""
    
    if(search!="" and len(idstotal)>0 and len(idsbrand)>0 ):
        products   = Product.objects.filter(Q(code__istartswith=search)| Q(name__istartswith=search)| Q(brand__name__istartswith=search) | Q(categories__name__istartswith=search) | Q(categories__code__istartswith=search)).filter(categories__pk__in=idstotal).filter(brand__pk__in=idsbrand).distinct()
    
    if(search!="" and len(idstotal)==0 and len(idsbrand)>0 ):
        products   = Product.objects.filter(Q(code__istartswith=search)| Q(name__istartswith=search)| Q(brand__name__istartswith=search) | Q(categories__name__istartswith=search) | Q(categories__code__istartswith=search)).filter(brand__pk__in=idsbrand).distinct()
    
    if(search!="" and len(idstotal)>0 and len(idsbrand)==0 ):
        products   = Product.objects.filter(Q(code__istartswith=search)| Q(name__istartswith=search)| Q(brand__name__istartswith=search) | Q(categories__name__istartswith=search) | Q(categories__code__istartswith=search)).filter(categories__pk__in=idstotal).distinct()
    
    if(search!="" and len(idstotal)==0 and len(idsbrand)==0 ):
        products   = Product.objects.filter(Q(code__istartswith=search)| Q(name__istartswith=search)| Q(brand__name__istartswith=search) | Q(categories__name__istartswith=search) | Q(categories__code__istartswith=search)).distinct()
    
    if(search=="" and len(idstotal)>0 and len(idsbrand)>0 ):
        products   = Product.objects.filter(categories__pk__in=idstotal).filter(brand__pk__in=idsbrand).distinct()
    
    if(search=="" and len(idstotal)==0 and len(idsbrand)>0 ):
        products   = Product.objects.filter(brand__pk__in=idsbrand).distinct()
    
    if(search=="" and len(idstotal)>0 and len(idsbrand)==0 ):
        products   = Product.objects.filter(categories__pk__in=idstotal).distinct()
    
    if(search=="" and len(idstotal)==0 and len(idsbrand)==0 ):
        products   = Product.objects.all()
    
    # if(len(idstotal)>0):
    #     products   = Products.objects.
    #     #filter(Q(code__istartswith=search)| Q(name__istartswith=search)| Q(brand__name__istartswith=search) | Q(categories__name__istartswith=search) | Q(categories__code__istartswith=search))
    
    # if(len(idsbrand)>0):
    #     products   = products.objects.
    
    # for d in idstotal:
    #     print(d)
    
    serializer = ProductFullSerializer(products, many=True, context={"request": request})
    
    return Response({"products": serializer.data})


def findListCategory(pcategory, ids):
    categories = Category.objects.filter(parent=pcategory)
    
    if categories.count() > 0 :
        for cat in categories:
            findListCategory(cat, ids)
            #ids.append(ele)
         
    ids.append(pcategory.pk)
    
    return ids


@api_view(["POST"])
def searchProductCategory(request, search):
    products   = Product.objects.filter( Q(categories__code__istartswith=search))
    serializer = ProductFullSerializer(products, many=True, context={"request": request})
 
    return Response({"products": serializer.data})
    

@api_view(["POST"])
@permission_classes([IsAdminUser])
def associateProductCategory(request, pk):
    categories  = request.data
    productObj  = Product.objects.get(pk=pk)
    categoriesAdd = productObj.categories.all()
    
    for catAdd in categoriesAdd:
        productObj.categories.remove(catAdd);
    
    print(categories)
    for category in categories:
        if(category['id'] is not None):
            categoryObj = Category.objects.get(pk=int(category['id']))
            productObj.categories.add(categoryObj);
        
    return Response(True)


@api_view(["GET"])
@permission_classes([IsAdminUser])
def productSerialJson(request, pk):
    product = Product.objects.get(pk=pk)
    series = product.series
    series = series.split(",")
    json_data = []
    for se in series:
        json_data.append({
            "text": se, 
            "value" : se
        })
    return Response(json_data)