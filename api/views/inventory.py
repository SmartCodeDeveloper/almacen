from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Inventory, DetailInventory, Employee
from ..serializers import InventorySerializer, DetailInventorySerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser

class InventoryList(APIView):
    def get(self, request, format=None):
        invs          = Inventory.objects.all()
        serializer    = InventorySerializer(invs, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = InventorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class InventoryDetail(APIView):
    def get_object(self, pk):
        try:
            return Inventory.objects.get(pk=pk)
        except Inventory.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        inv  = self.get_object(pk)
        serializer   = InventorySerializer(inv)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        inv  = self.get_object(pk)
        serializer   = InventorySerializer(inv, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        inv = self.get_object(pk)
        inv.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
def inventory_employee(request):
    user        = request.user
    employeeObj = Employee.objects.filter(user=user).first()
    inventory   = Inventory.objects.filter(employee=employeeObj).first()
    details     = DetailInventory.objects.filter(inventory=inventory)
    serializer  = DetailInventorySerializer(details, many=True, context={"request": request})
    return Response(serializer.data)

@api_view(["GET"])
def inventory_employee_report(request, employee):
    employeeObj = Employee.objects.get(pk=employee)
    inventory   = Inventory.objects.filter(employee=employeeObj).first()
    details     = DetailInventory.objects.filter(inventory=inventory)
    serializer  = DetailInventorySerializer(details, many=True, context={"request": request})
    return Response(serializer.data)
