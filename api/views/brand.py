from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape
from django.db.models import Q
from ..models import Brand
from ..serializers import BrandSerializer, BrandSaveSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser

class BrandList(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAdminUser]
    
    def get(self, request, format=None):
        brands        = Brand.objects.all()
        serializer    = BrandSerializer(brands, many=True, context={"request": request})
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = BrandSaveSerializer(data=request.data)
        if serializer.is_valid():
            name           = serializer.validated_data["name"]
            description    = serializer.validated_data["description"]
            active         = serializer.validated_data["active"]
            
            photo = None
            if "photo" in serializer.validated_data:
                photo = serializer.validated_data["photo"]
            

            
            brandNew       = Brand.objects.create(name=name, description=description, active=active, photo=photo)
            serializerNew  =  BrandSerializer(brandNew, context={"request": request} )
            
            return Response(serializerNew.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BrandDetail(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAdminUser]
    
    def get_object(self, pk):
        try:
            return Brand.objects.get(pk=pk)
        except Brand.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        brand  = self.get_object(pk)
        serializer   = BrandSerializer(brand,  context={"request": request})
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        brand  = self.get_object(pk)
        serializer   = BrandSaveSerializer(brand, data=request.data)
        if serializer.is_valid():
            name           = serializer.validated_data["name"]
            description    = serializer.validated_data["description"]
            active         = serializer.validated_data["active"]
            
            photo = None
            if "photo" in serializer.validated_data:
                photo = serializer.validated_data["photo"]

            
            brand.name = name
            brand.description = description
            brand.active = active 
            
            if photo is not None:
                brand.photo = photo 
            
            brand.save()
            serializerNew  =  BrandSerializer(brand, context={"request": request} )
            
            return Response(serializerNew.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        brand = self.get_object(pk)
        brand.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderListBrandJson(BaseDatatableView):
    order_columns = ['name', 'description',]

    def get_initial_queryset(self):
        return  Brand.objects.all()

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        if search:
            print(search)
            qs = qs.filter(Q(name__istartswith=search)| Q(description__istartswith=search))

        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            
            status = item.active 
            
            statusHtml = "Inactivo"
            
            if(status):
                statusHtml = "Activo"
                
            
            json_data.append([
                escape("{0}".format(item.id)),
                escape("{0}".format(item.name)),  
                escape("{0}".format(item.description)), 
                statusHtml,
                '<i data-id="{0}"  class="la la-pencil-square ico-edit js-edit"></i>'.format(item.id),
                '<i data-id="{0}"class="la la-trash ico-trash js-delete"></i>'.format(item.id),
            ])
            
        return json_data


@api_view(["GET"])
def brandAll(request):
    brands     = Brand.objects.all()
    serializer = BrandSerializer(brands, many=True, context={"request": request})
    return Response(serializer.data)




@api_view(["GET"])
@permission_classes([IsAdminUser])
def brandJson(request):
    brands = Brand.objects.all()
    json_data = []
    for brand in brands:
        json_data.append({
            "text": brand.name, 
            "value" : brand.id
        })
    return Response(json_data)