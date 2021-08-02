from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Order, DetailOrder, Product, Employee, Inventory, DetailInventory, Manifest, DetailManifest
from ..serializers import OrderSerializer, Order2Serializer, OrderFullSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape
from django.db.models import Q
from django.db import transaction
from decimal import Decimal

class OrderList(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request, format=None):
        orders        = Order.objects.all()
        serializer    = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):

        
        serializer = OrderSerializer(data=request.data)
        haveDetail = False 
        
        if "details" in request.data:
            haveDetail = True
            
        if serializer.is_valid() and haveDetail:
            
            
            priority    = serializer.validated_data["priority"]
            statusOp    = 1
            torder      = serializer.validated_data["torder"]
            tpayment    = serializer.validated_data["tpayment"]
            
            description = None
            if "description" in serializer.validated_data:
                description = serializer.validated_data["description"]
            
            employee = None
            if "employee" in serializer.validated_data:
                employee = serializer.validated_data["employee"]
            
            date_delivery = None
            if "date_delivery" in serializer.validated_data:
                date_delivery = serializer.validated_data["date_delivery"]
            
            
            with transaction.atomic():
                
                orderNew = Order.objects.create(date_delivery=date_delivery, employee=employee, status=statusOp, priority=priority, torder=torder, tpayment=tpayment, description=description)
                details = request.data['details']
                
                for det in details:
                    productObj = Product.objects.get(pk=det['product'])
                    
                    quantity   = Decimal(det['quantity'])
                    price      = Decimal(det['price'])
                    total      = Decimal(det['total'])
                    seriales   = None
                        
                    if det['series']!="" and det['series']!=None:
                        seriales =  det['series']
                        
                    detNew     = DetailOrder.objects.create(order=orderNew, product=productObj, quantity=quantity , price=price , total=total, seriales=seriales )
                    
                    if(torder==1):
                        productObj.stock = productObj.stock  - detNew.quantity
                    else:
                        productObj.stock = productObj.stock  + detNew.quantity
                    
                    productObj.save()
                    
                serializerNew =  OrderSerializer(orderNew)
                return Response(serializerNew.data, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderDetail(APIView):
    permission_classes = [IsAdminUser]
    
    def get_object(self, pk):
        try:
            return Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        order  = self.get_object(pk)
        serializer   = Order2Serializer(order)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        
        order  = self.get_object(pk)
        print(request.data)
        serializer   = OrderSerializer(order, data=request.data)
        haveDetail = False 
        
        if "details" in request.data:
            haveDetail = True
            
        if serializer.is_valid() and haveDetail:
            
            priority    = serializer.validated_data["priority"]
            #statusOp    = serializer.validated_data["status"]
            torder        = serializer.validated_data["torder"]
            tpayment      = serializer.validated_data["tpayment"]
            
            description = None
            if "description" in serializer.validated_data:
                description = serializer.validated_data["description"]
            
            employee = None
            if "employee" in serializer.validated_data:
                employee = serializer.validated_data["employee"]
            
            date_delivery = None
            if "date_delivery" in serializer.validated_data:
                date_delivery = serializer.validated_data["date_delivery"]
            
            
            with transaction.atomic():
                
                order.date_delivery = date_delivery
                order.employee      = employee
                #order.status        = statusOp
                order.priority      = priority
                order.torder        = torder
                order.description   = description
                order.tpayment      = tpayment
                
                order.save()
                
                details = request.data['details']
                  
                for det in details:
                    
                    productObj = Product.objects.get(pk=det['product'])              
                    
                    if(det['id']!= 0):
                        detaObj          = DetailOrder.objects.get(pk=det['id'])
                        oldquantity      = detaObj.quantity
                        detaObj.product  = productObj
                        detaObj.quantity = Decimal(det['quantity'])
                        detaObj.price    = Decimal(det['price'])
                        detaObj.total    = Decimal(det['total'])
                        
                        if det['series']!="" and det['series']!=None:
                            detaObj.seriales =  det['series']
                        else:
                            detaObj.seriales =  None
                            
                        detaObj.save()
                        
                        if(torder==1):
                            productObj.stock = productObj.stock + oldquantity - detaObj.quantity
                        else:
                            productObj.stock = productObj.stock - oldquantity + detaObj.quantity
                        
                        productObj.save()
                    else:
                        quantity   = Decimal(det['quantity'])
                        price      = Decimal(det['price'])
                        total      = Decimal(det['total'])
                        seriales   = None
                        
                        if det['series']!="" and det['series']!=None:
                            seriales =  det['series']

                        detNew = DetailOrder.objects.create(order=order, seriales=seriales, product=productObj, quantity=quantity , price=price , total=total )
                        
                        if(torder==1):
                            productObj.stock = productObj.stock - detNew.quantity
                        else:
                            productObj.stock = productObj.stock + detNew.quantity
                        
                        productObj.save()
                
                serializerNew =  OrderSerializer(order)
                return Response(serializerNew.data)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        order = self.get_object(pk)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)





# class Order(models.Model):
#     employee  = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)
#     priority  = models.IntegerField(default=1)
#     status    = models.IntegerField(default=1)
#     date_delivery = models.DateField(null=True, blank=True)
#     date_created  = models.DateTimeField(auto_now_add=True)
#     date_updated  = models.DateTimeField(auto_now=True)

class OrderListOrdenJson(BaseDatatableView):
    order_columns = ['-id']

    def get_initial_queryset(self):
        return  Order.objects.all()

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        if search:
            print(search)
            qs = qs.filter(Q(employee__name__istartswith=search)| Q(employee__lastname__istartswith=search) | Q(employee__lastname__istartswith=search)  | Q(date_created__date=search))

        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            
            priority    = item.priority 
            statusOrden = item.status 
            
            priorityHtml = ""
            if priority==1:
                priorityHtml = '<span data-id="{0}" class="badge badge-light-secondary js-change-priority">Baja</span>'.format(item.id);
            elif priority==2:
                priorityHtml = '<span data-id="{0}" class="badge badge-light-warning js-change-priority">Media</span>'.format(item.id);
            elif priority==3:
                priorityHtml = '<span data-id="{0}" class="badge badge-light-danger js-change-priority">Alta</span>'.format(item.id);
            
            statusHtml = ""
            if statusOrden==1:
                statusHtml = '<span data-id="{0}" class="badge badge-warning js-change-status">Pendiente</span>'.format(item.id);
            elif statusOrden==2:
                statusHtml = '<span data-id="{0}" class="badge badge-success js-change-status" >Aprobado</span>'.format(item.id);
            elif statusOrden==3:
                statusHtml = '<span data-id="{0}" class="badge badge-danger js-change-status">Negado</span>'.format(item.id);
            elif statusOrden==4:
                statusHtml = '<span data-id="{0}" class="badge badge-success js-change-status" >Entregado</span>'.format(item.id);
                            
            
            tipoHtml = ""
            
            if item.torder == 1:
                tipoHtml = "Pedido"
            else:
                tipoHtml = "Devolución"
            
            tipopago = ""
            
            if item.tpayment == 1:
                tipopago = "Crédito"
            else:
                tipopago = "Débito"
                
            
            #manifest     = Manifest.objects.filter(order=item).first()
            
            employeeHtml = ""
            
            if item.employee:
                employeeHtml = "{0} {1}".format(item.employee.name, item.employee.lastname)

                            
            json_data.append([
                escape("{0}".format(item.id)),
                "{0}/{1}/{2}".format(item.date_created.day, item.date_created.month, item.date_created.year),
                employeeHtml,
                tipoHtml,
                priorityHtml, 
                statusHtml,
                "{0}".format(tipopago),
                '<i data-id="{0}"  class="la la-folder ico-edit js-manifiesto"></i>'.format(item.id),
                '<i data-id="{0}"  class="la la-pencil-square ico-edit js-edit"></i>'.format(item.id),
                '<i data-id="{0}"class="la la-trash ico-trash js-delete"></i>'.format(item.id),
            ])
            
        return json_data


@api_view(["POST"])
@permission_classes([IsAdminUser])
def changeOrder(request, order):
    print(request.data)
    
    statusN       = request.data['status']
    statusN       = int(statusN)
    priority      = request.data['priority']
    date_delivery  = None
    date_delivery2 = None
    hour_delivery  = None
    
    if (("date_delivery" in request.data) and (request.data["date_delivery"]!="")):
        date_delivery = request.data["date_delivery"]
    
    if (("date_delivery2" in request.data) and (request.data["date_delivery2"]!="")):
        date_delivery2 = request.data["date_delivery2"]
    
    if (("hour_delivery" in request.data) and (request.data["hour_delivery"]!="")):
        hour_delivery = request.data["hour_delivery"]
    
    orderObj = Order.objects.get(pk=order)
    invObj  = Inventory.objects.filter(employee=orderObj.employee).first()
    if(invObj is None):
        invObj  = Inventory.objects.create(employee=orderObj.employee)
    
        
    detailsOrder = DetailOrder.objects.filter(order=orderObj)

    print("=========")
    print(statusN)
    print(orderObj.torder)
    print("============")
    if(statusN == 2 and orderObj.torder==1): #Orden Pedido Aprobado
        print(detailsOrder)
        print("entreo 1")
        
        manifest = Manifest.objects.filter(order=orderObj).first()
        if manifest is None:
            manifest = Manifest.objects.create(employee=orderObj.employee, order=orderObj)
        
        detailsManifest = DetailManifest.objects.filter(manifest=manifest)
        detailsManifest.delete()
            
        for det in detailsOrder:
            print("Orden Pedido Aprobado")
            productObj = det.product
            detailInv = DetailInventory.objects.filter(inventory=invObj,product=det.product).first()
            if detailInv is None:
                DetailInventory.objects.create(inventory=invObj, product=productObj, quantity=det.quantity)
            else:
                detailInv.quantity = detailInv.quantity + det.quantity
                detailInv.save()
            
            DetailManifest.objects.create(manifest=manifest, product=det.product, quantity=det.quantity)
    
    if(statusN == 3 and orderObj.torder==1):  #Orden Pedido Negado
        print("entro 2")
        for det in detailsOrder:
            print("Orden Pedido Negago")
            productObj = det.product
            productObj.stock = productObj.stock + det.quantity 
            productObj.save()
                
    if(statusN == 2 and orderObj.torder==2):  #Devolución Aprobada
        print("entro 3")      
        for det in detailsOrder:
            print("Devolucion Aprobada")
            productObj = det.product
            detailInv = DetailInventory.objects.filter(inventory=invObj, product=productObj).first()
            if detailInv:
                detailInv.quantity = detailInv.quantity - det.quantity
                detailInv.save()
    
            
    orderObj.status = statusN 
    orderObj.priority = priority
    orderObj.date_delivery = date_delivery
    orderObj.date_delivery2 = date_delivery2
    orderObj.hour_delivery  = hour_delivery
    
    
    orderObj.save()
    
    
    return Response(True)


@api_view(["DELETE"])
@permission_classes([IsAdminUser])
def removeDetail(request, pk):
    detailObj = DetailOrder.objects.get(pk=pk)
    detailObj.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
def ordersEmployee(request):
    user = request.user 
    employee   = Employee.objects.filter(user=user).first()
    print(employee.user.email)
    orders     = Order.objects.filter(employee=employee, status=1)
    ordersfinalizadas = Order.objects.filter(employee=employee, status__in=[2,3])
    serializerPendiente  = OrderFullSerializer(orders, many=True, context={"request": request})
    serializerFinalizada = OrderFullSerializer(ordersfinalizadas, many=True, context={"request": request})
    return Response({"pendientes": serializerPendiente.data, "finalizadas": serializerFinalizada.data })