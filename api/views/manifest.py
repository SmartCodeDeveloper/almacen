from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Product, Employee, Manifest, DetailManifest
from ..serializers import ManifestSerializer, ManifestFullSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape
from django.db.models import Q
from django.db import transaction
from decimal import Decimal

class ManifestList(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request, format=None):
        manifests     = Manifest.objects.all()
        serializer    = ManifestSerializer(manifests, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = ManifestSerializer(data=request.data)
        haveDetail = False 
        
        if "details" in request.data:
            haveDetail = True
            
        if serializer.is_valid() and haveDetail:
            
            employee           = serializer.validated_data["employee"]
            date_manifest      = serializer.validated_data["date_manifest"]
            receive            = serializer.validated_data["receive"]
            delivery           = serializer.validated_data["delivery"]
            order              = None
            
            if "order" in serializer.validated_data:
                order = serializer.validated_data["order"]
            
            
            description = None
            if "description" in serializer.validated_data:
                description = serializer.validated_data["description"]
            
            
            with transaction.atomic():
                
                manifestNew = Manifest.objects.create(date_manifest=date_manifest, employee=employee, description=description, receive=receive, delivery=delivery, order=order)
                details     = request.data['details']
                
                for det in details:
                    productObj = Product.objects.get(pk=det['product'])
                    quantity   = Decimal(det['quantity'])
                    seriales   = None
                        
                    if det['series']!="" and det['series']!=None:
                        seriales =  det['series']
                        
                    detNew     = DetailManifest.objects.create(manifest=manifestNew, product=productObj, quantity=quantity, seriales=seriales)
                    
                serializerNew =  ManifestSerializer(manifestNew)
                return Response(serializerNew.data, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ManifestDetail(APIView):
    permission_classes = [IsAdminUser]
    
    def get_object(self, pk):
        try:
            return Manifest.objects.get(pk=pk)
        except Manifest.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        manifest     = self.get_object(pk)
        serializer   = ManifestSerializer(manifest)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        
        manifest  = self.get_object(pk)
        print(request.data)
        serializer   = ManifestSerializer(manifest, data=request.data)
        haveDetail = False 
        
        if "details" in request.data:
            haveDetail = True
            
        if serializer.is_valid() and haveDetail:
            
            employee           = serializer.validated_data["employee"]
            date_manifest      = serializer.validated_data["date_manifest"]
            
            description = None
            if "description" in serializer.validated_data:
                description = serializer.validated_data["description"]
            
            
            with transaction.atomic():
                
                manifest.date_manifest = date_manifest
                manifest.employee      = employee
                manifest.description   = description
                
                manifest.save()
                
                details = request.data['details']
                  
                for det in details:
                    
                    productObj = Product.objects.get(pk=det['product']) 
                    
                                 
                    
                    if(det['id']!= 0):
                        detaObj          = DetailManifest.objects.get(pk=det['id'])
                        detaObj.product  = productObj
                        detaObj.quantity = Decimal(det['quantity'])
                        
                        if det['series']!="" and det['series']!=None:
                            detaObj.seriales =  det['series']
                        else:
                            detaObj.seriales =  None
                            
                        detaObj.save()
                        
                        
                        
                    else:
                        quantity   = Decimal(det['quantity'])
                        seriales   = None
                        
                        if det['series']!="" and det['series']!=None:
                            seriales =  det['series']
                            
                        detNew     = DetailManifest.objects.create(manifest=manifest, product=productObj, quantity=quantity, seriales=seriales)
                        
                serializerNew =  ManifestSerializer(manifest)
                return Response(serializerNew.data)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        manifest = self.get_object(pk)
        manifest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




class OrderListManifestJson(BaseDatatableView):
    order_columns = ['-id']

    def get_initial_queryset(self):
        return  Manifest.objects.all()

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        if search:
            print(search)
            qs = qs.filter(Q(employee__name__istartswith=search)| Q(employee__lastname__istartswith=search) | Q(employee__lastname__istartswith=search)  | Q(date_manifest__date=search))

        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            
            statusManifest = item.printer 
            
            statusHtml = ""
            if statusManifest:
                statusHtml = '<span data-id="{0}" class="badge badge-success js-change-status" >Impreso</span>'.format(item.id);
            else:
                statusHtml = '<span data-id="{0}" class="badge badge-danger js-change-status"> No Impreso</span>'.format(item.id);
                            
            date_manifest = ""
            if item.date_manifest:
                date_manifest = "{0}/{1}/{2}".format(item.date_manifest.day, item.date_manifest.month, item.date_manifest.year)
                
            
            json_data.append([
                escape("{0}".format(item.id)),
                date_manifest,
                "{0} {1}".format(item.employee.name, item.employee.lastname),
                statusHtml, 
                '<i data-id="{0}"  class="fa fa-eye ico-edit js-edit"></i>'.format(item.id),
                '<i data-id="{0}"  class="la la-trash ico-trash js-delete"></i>'.format(item.id),
            ])
            
        return json_data

@api_view(["POST"])
@permission_classes([IsAdminUser])
def changeManifest(request, manifest):
    manifestObj = Manifest.objects.get(pk=manifest)
    manifestObj.printer = True 
    manifestObj.save()
    return Response(True)