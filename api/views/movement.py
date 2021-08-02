from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape
from django.db.models import Q
from ..models import Movement, DetailMov, Employee, Product, Inventory, DetailInventory
from ..serializers import MovementClientSerializer, DetailCreateSerializer, MovementSerializer, Movement2Serializer, DetailMovementSerializer, ReportMovSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.parsers import MultiPartParser, FormParser
import json




class OrderListTransferJson(BaseDatatableView):
    order_columns = ['-datemov',]

    def get_initial_queryset(self):
        return  Movement.objects.filter(typemov=2)

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        if search:
            print(search)
            qs = qs.filter(Q(fromemployee__name__istartswith=search)| Q(toemployee__name__istartswith=search))

        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            
            observations = item.observations 
            status       = item.status
            
            if(observations is None):
                observations = ""
            
            
            statusHtml = ""
            if status==1:
                statusHtml = '<span data-id="{0}" class="badge badge-warning js-change-status">Pendiente</span>'.format(item.id);
            elif status==2:
                statusHtml = '<span data-id="{0}" class="badge badge-success js-change-status" >Aprobado</span>'.format(item.id);
            elif status==3:
                statusHtml = '<span data-id="{0}" class="badge badge-danger js-change-status" >Negada</span>'.format(item.id);
                
            
            json_data.append([
                "{0}/{1}/{2}".format(item.datemov.day, item.datemov.month, item.datemov.year),
                escape("{0} {1}".format(item.fromemployee.name, item.fromemployee.lastname )),  
                escape("{0} {1}".format(item.toemployee.name, item.toemployee.lastname)), 
                escape("{0}".format(observations)),
                statusHtml,
                '<button data-id="{0}" type="button" class="btn btn-danger waves-effect waves-light js-ver-detail"><i class="mdi mdi-file-document"></i></button>'.format(item.id),
            ])
            
        return json_data



@api_view(["POST"])
def create_movement(request):
    user         = request.user
    employeeObj  = Employee.objects.filter(user=user).first()
    images_data  = request.FILES
    data         = request.data
    details      = data['details']
    client       = data['client']
    typemov      = data['typemov']
    sign         = images_data['file']
    observations = None
    
    
    if "observations" in data:
        observations = data["observations"]
        
    
    movementObj  = Movement.objects.create(fromemployee=employeeObj, client=client, sign=sign, typemov=typemov, observations=observations)
    invObj       = Inventory.objects.filter(employee=employeeObj).first()
    
    detailsArray = json.loads(details)
    #print(json.loads(details))
    #print(len(detailsN))
    #print(images_data['file'])
    #print(request.data)
    
    #print(data['client'])
    #print(data['observations'])
    
    for deta in detailsArray:
        quantity   = int(deta['quantity'])
        productId  = int(deta['product'])
        seriales   = deta["seriales"]
        productObj = Product.objects.get(pk=productId)
        detailInv  = DetailInventory.objects.filter(product=productObj, inventory=invObj).first()
        DetailMov.objects.create(movement=movementObj, quantity=quantity, product=productObj, seriales=seriales)
        detailInv.quantity = detailInv.quantity - quantity
        detailInv.save()
    
    return Response(True)


@api_view(["POST"])
def create_transference(request):
    user         = request.user
    employeeObj  = Employee.objects.filter(user=user).first()
    data         = request.data
    print(data)
    details      = data['details']
    client       = int(data['client'])
    typemov      = data['typemov']
    observations = None
    #userto       = User.objects.filter(username=client).first()
    #toemployee   = Employee.objects.filter(user=userto).first()
    toemployee   = Employee.objects.get(pk=client)
    
    print("llefandaosodoaso")
    
    
    if "observations" in data:
        observations = data["observations"]
    
    
    if(toemployee):
        movementObj  = Movement.objects.create(fromemployee=employeeObj, toemployee=toemployee, client=toemployee.user.username, typemov=typemov, observations=observations, status=1)
        invObj       = Inventory.objects.filter(employee=employeeObj).first()
        invObjTo     = Inventory.objects.filter(employee=toemployee).first()
        detailsArray = details
        
        #print(json.loads(details))
        #print(len(detailsN))
        #print(images_data['file'])
        #print(request.data)
        
        #if(invObjTo is None):
        #    invObjTo  = Inventory.objects.create(employee=toemployee)
        
        #print(data['client'])
        #print(data['observations'])
        
        for deta in detailsArray:
            
            quantity   = int(deta['quantity'])
            productId  = int(deta['product'])
            seriales   = deta["seriales"]
            
            productObj = Product.objects.get(pk=productId)
            detailInv  = DetailInventory.objects.filter(product=productObj, inventory=invObj).first()
            DetailMov.objects.create(movement=movementObj, quantity=quantity, product=productObj, seriales=seriales)
            
            detailInv.quantity = detailInv.quantity - quantity
            detailInv.save()
            
            #if(invObjTo):
            #    detailInvTo  = DetailInventory.objects.filter(product=productObj, inventory=invObjTo).first()
            #    if(detailInvTo is None):
            #        DetailInventory.objects.create(product=productObj, inventory=invObjTo, quantity=quantity)
            #    else:
            #        detailInvTo.quantity = detailInvTo.quantity + quantity
            #        detailInvTo.save()
                    
        
        return Response(True)
    return Response(False)

@api_view(["GET"])
def my_movement(request, typemov):
    user         = request.user
    employeeObj  = Employee.objects.filter(user=user).first()
    movements    = Movement.objects.filter(fromemployee=employeeObj, typemov=typemov).order_by('-datemov')
    serializer   = MovementSerializer(movements, many=True, context={"request": request})
    return Response(serializer.data)

@api_view(["GET"])
def detail_mov(request, mov):
    user         = request.user
    #employeeObj  = Employee.objects.filter(user=user).first()
    movObj       = Movement.objects.get(pk=mov)
    details      = DetailMov.objects.filter(movement=movObj)
    serializer   = DetailMovementSerializer(details, many=True, context={"request": request})
    return Response(serializer.data)

@api_view(["GET"])
def get_transfer(request, mov):
    user         = request.user
    movObj       = Movement.objects.get(pk=mov)
    serializer   = MovementSerializer(movObj, context={"request": request})
    return Response(serializer.data)
    

@api_view(["POST"])
def changeTransference(request, mov):
    status       = int(request.data['status'])
    movObj       = Movement.objects.get(pk=mov)
    details      = DetailMov.objects.filter(movement=movObj)
    
    
    print("Aca status")
    print(status)
    
    if status==2:
        
        #invObj       = Inventory.objects.filter(employee=employeeObj).first()
        invObjTo     = Inventory.objects.filter(employee=movObj.toemployee).first()
        
        if(invObjTo is None):
            invObjTo  = Inventory.objects.create(employee=movObj.toemployee)
            
        print("pasando a aprobar")
        print(details)
        
        for deta in details:
            print("entro en for")
            if(invObjTo):
               detailInvTo  = DetailInventory.objects.filter(product=deta.product, inventory=invObjTo).first()
               if(detailInvTo is None):
                   DetailInventory.objects.create(product=deta.product, inventory=invObjTo, quantity=deta.quantity)
               else:
                   detailInvTo.quantity = detailInvTo.quantity + deta.quantity
                   detailInvTo.save()
        
        movObj.status = status
        movObj.save()
                   
    elif status==3:
        invObjFrom     = Inventory.objects.filter(employee=movObj.fromemployee).first()
        
        if(invObjFrom is None):
            invObjFrom  = Inventory.objects.create(employee=movObj.fromemployee)
            
        print("pasando a aprobar")
        print(details)
        
        for deta in details:
            print("entro en for")
            if(invObjFrom):
               detailInvFrom  = DetailInventory.objects.filter(product=deta.product, inventory=invObjFrom).first()
               if(detailInvFrom is None):
                   DetailInventory.objects.create(product=deta.product, inventory=invObjFrom, quantity=deta.quantity)
               else:
                   detailInvFrom.quantity = detailInvFrom.quantity + deta.quantity
                   detailInvFrom.save()
        
        movObj.status = status
        movObj.save()
        
    else:
        movObj.status = status
        movObj.save()
        
    return Response(True)
        

@api_view(["POST"])
def detail_mov_report(request):
    user         = request.user
    serializer   = ReportMovSerializer(data=request.data)
    movements    = []
    
    if serializer.is_valid():
        print(serializer.validated_data)
        employee = serializer.validated_data["employee"]
        typemov  = serializer.validated_data["typemov"]
        datefrom = serializer.validated_data["datefrom"]
        dateto   = serializer.validated_data["dateto"]
        serie    = serializer.validated_data["serie"]
        
        
        
        if employee==0:
            if(typemov==0):
                if serie=="ninguna":
                    movements = Movement.objects.filter(datemov__date__gte=datefrom, datemov__date__lte=dateto).order_by('datemov')
                else:
                    movements    = []
                    movementsAux = Movement.objects.filter(datemov__date__gte=datefrom, datemov__date__lte=dateto).order_by('datemov')
                    for mov in movementsAux:
                        details      = DetailMov.objects.filter(seriales__icontains=serie, movement=mov).count()
                        if details>0:
                            movements.append(mov)
                        
                        
            else:
                if serie=="ninguna":
                    movements = Movement.objects.filter(typemov=typemov,  datemov__date__gte=datefrom, datemov__date__lte=dateto).order_by('datemov')
                else:
                    movements    = []
                    movementsAux = Movement.objects.filter(datemov__date__gte=datefrom, datemov__date__lte=dateto).order_by('datemov')
                    for mov in movementsAux:
                        details      = DetailMov.objects.filter(seriales__icontains=serie, movement=mov).count()
                        if details>0:
                            movements.append(mov)
                    
        else:
            employeeObj = Employee.objects.get(pk=employee)
            if(typemov==0):
                if serie=="ninguna":
                    movements = Movement.objects.filter(fromemployee=employeeObj, datemov__date__gte=datefrom, datemov__date__lte=dateto).order_by('datemov')
                else:
                    movements    = []
                    movementsAux = Movement.objects.filter(datemov__date__gte=datefrom, datemov__date__lte=dateto).order_by('datemov')
                    for mov in movementsAux:
                        details      = DetailMov.objects.filter(seriales__icontains=serie, movement=mov).count()
                        if details>0:
                            movements.append(mov)
                    
            else:
                if serie=="ninguna":
                    movements = Movement.objects.filter(fromemployee=employeeObj, typemov=typemov,  datemov__date__gte=datefrom, datemov__date__lte=dateto).order_by('datemov')
                else:
                    movements    = []
                    movementsAux = Movement.objects.filter(datemov__date__gte=datefrom, datemov__date__lte=dateto).order_by('datemov')
                    for mov in movementsAux:
                        details      = DetailMov.objects.filter(seriales__icontains=serie, movement=mov).count()
                        if details>0:
                            movements.append(mov)
                    
        
        serializerResp = Movement2Serializer(movements, many=True, context={"request": request})
        
        return Response(serializerResp.data)
        
        #employeeObj  = Employee.objects.filter(user=user).first()
        #movObj       = Movement.objects.get()
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


