from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Cart, Employee, DetailCart, Order, DetailOrder, Product
from ..serializers import CartSerializer, CartDetailSerializer, CartDetailFullSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser


@api_view(["GET"])
def getCart(request):
    user = request.user
    employee = Employee.objects.filter(user=user).first()
    
    if employee:
        cartObj = Cart.objects.filter(employee=employee).first()
        
        if(cartObj is None):
            cartObj    = Cart.objects.create(employee=employee)
        
        details = DetailCart.objects.filter(cart=cartObj)
        
        serializer = CartSerializer(cartObj)
        serializerDetail = CartDetailFullSerializer(details, many=True, context={"request": request})
        
        return Response({"cart": serializer.data, "details": serializerDetail.data})
    
    return Response("error: not employee", status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def addDetailCart(request):
    serializer = CartDetailSerializer(data=request.data)
    if serializer.is_valid():
        cart              = serializer.validated_data["cart"]
        product           = serializer.validated_data["product"]
        quantity          = serializer.validated_data["quantity"]
        price             = serializer.validated_data["price"]
        total             = serializer.validated_data["total"]
        
        
        detaOld           = DetailCart.objects.filter(product=product, cart=cart).first()
        
        if(detaOld):
            
            if(product.stock > quantity):
                
                product.stock = product.stock - quantity
                product.save()
                
                detaOld.quantity = detaOld.quantity + quantity
                detaOld.price    = price 
                detaOld.total    = detaOld.quantity * detaOld.price
                detaOld.save()
                
                return Response(True)
        else:
            if product.stock >= quantity:
                detaObj = DetailCart.objects.create(cart=cart, product=product, quantity=quantity, price=price, total=total)
                product.stock = product.stock - quantity
                product.save()
        
                return Response(True)
    
    return Response(False)

@api_view(["POST"])
def restDetailCart(request):
    serializer = CartDetailSerializer(data=request.data)
    if serializer.is_valid():
        cart              = serializer.validated_data["cart"]
        product           = serializer.validated_data["product"]
        quantity          = serializer.validated_data["quantity"]
        price             = serializer.validated_data["price"]
        total             = serializer.validated_data["total"]
        
        
        detaOld           = DetailCart.objects.filter(product=product, cart=cart).first()
        
        if(detaOld):
            
            if(product.stock > quantity):
                
                product.stock = product.stock + quantity
                product.save()
                
                detaOld.quantity = detaOld.quantity - quantity
                detaOld.price    = price 
                detaOld.total    = detaOld.quantity * detaOld.price
                detaOld.save()
                
                return Response(True)
        else:
            if product.stock >= quantity:
                detaObj = DetailCart.objects.create(cart=cart, product=product, quantity=quantity, price=price, total=total)
                product.stock = product.stock + quantity
                product.save()
        
                return Response(True)
    
    return Response(False)        

    
@api_view(["DELETE"])
def removeDetailCart(request, pk):
    deta = DetailCart.objects.get(pk=pk)
    
    productObj = deta.product 
    productObj.stock = productObj.stock + deta.quantity
    productObj.save()
    
    deta.delete()
    return Response(True)


@api_view(["POST"])
def processCart(request, tpayment):
    user = request.user
    employee = Employee.objects.filter(user=user).first()
    cart    = Cart.objects.filter(employee=employee).first()
    details = DetailCart.objects.filter(cart=cart)
    
    if details.count() > 0:
        orderObj = Order.objects.create(employee=employee, tpayment=tpayment)
        
        for deta in details:
            detaNew = DetailOrder.objects.create(order=orderObj, product=deta.product, quantity=deta.quantity, price=deta.price, total=deta.total)
        
        details.delete()
        
        return Response(True)
    
    return Response(False)

        
