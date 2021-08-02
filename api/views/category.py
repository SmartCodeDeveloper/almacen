from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape
from django.db.models import Q
from ..models import Category, Product
from ..serializers import CategorySerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.parsers import MultiPartParser, FormParser

class CategoryList(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request, format=None):
        categories     = Category.objects.all()
        serializer     = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = CategorySerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
         
            name    = serializer.validated_data["name"]
            code    = serializer.validated_data["code"]
            active  = serializer.validated_data["active"]
            
            parent = None
            if "parent" in serializer.validated_data:
                parent = serializer.validated_data["parent"]
                code   = parent.code+" "+ code
                
            
            categoryFind    = Category.objects.filter(code=code).first()
            
            if(categoryFind is None):
                categoryNew     = Category.objects.create(parent=parent, name=name, code=code, active=active)
                serializer      = CategorySerializer(categoryNew)

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response("codigo de producto existe", status=status.HTTP_406_NOT_ACCEPTABLE)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryDetail(APIView):
    permission_classes = [IsAdminUser]
    
    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        category  = self.get_object(pk)
        serializer   = CategorySerializer(category)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        category       = self.get_object(pk)
        serializer     = CategorySerializer(category, data=request.data)
        
        if serializer.is_valid():

            name    = serializer.validated_data["name"]
            code    = serializer.validated_data["code"]
            active  = serializer.validated_data["active"]
            
            parent = None
            if "parent" in serializer.validated_data:
                parent = serializer.validated_data["parent"]
            
            
            categoryFind    = Category.objects.filter(code=code).first()
            
            if((categoryFind is None) or (categoryFind==category)):
                
                category.name    = name
                category.code    = code
                category.active  = active
                category.parent  = parent
                category.save()
                
                return Response(serializer.data)
            else:
                return Response("codigo de categoría ya existe", status=status.HTTP_406_NOT_ACCEPTABLE)
            
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        category = self.get_object(pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderListCategoryJson(BaseDatatableView):
    order_columns = ['code',]

    def get_initial_queryset(self):
        return  Category.objects.all()

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        level  = self.request.GET.get('parent')
        
        print("LEVEL")
        print(level)
        if(level=="0"):
            print("entro aca")
            qs = qs.filter(parent__isnull=True)
        else:
            qs = qs.filter(parent=level)
        
        
        if search:
            print(search)
            qs = qs.filter(Q(code__istartswith=search)| Q(name__istartswith=search))

        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            
            status = item.active 
            
            statusHtml = "Inactivo"
            
            if(status):
                statusHtml = "Activo"
            
            
            quantity = Product.objects.filter(categories__pk=item.id).count()
                
            
            json_data.append([
                '<a href="/categorias/{0}">{1}</a>'.format(item.id, item.code),  
                escape("{0}".format(item.name)), 
                statusHtml,
                '<a href="/productos-categoria/{0}">{1}</a>'.format(item.id, quantity),
                '<i data-id="{0}"  class="la la-pencil-square ico-edit js-edit"></i>'.format(item.id),
                '<i data-id="{0}"class="la la-trash ico-trash js-delete"></i>'.format(item.id),
            ])
            
        return json_data

@api_view(["GET"])
def categoryAll(request):
    categories = Category.objects.filter(parent__isnull=True)
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAdminUser])
def categoryJson(request):
    categories = Category.objects.all()
    json_data = []
    for category in categories:
        json_data.append({
            "text": category.code + " " +category.name, 
            "value" : category.id
        })
    return Response(json_data)