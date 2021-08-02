from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Unit
from ..serializers import UnitSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser

class UnitList(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request, format=None):
        units      = Unit.objects.all()
        serializer    = UnitSerializer(units, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = UnitSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UnitDetail(APIView):
    permission_classes = [IsAdminUser]
    
    def get_object(self, pk):
        try:
            return Unit.objects.get(pk=pk)
        except Unit.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        unit  = self.get_object(pk)
        serializer   = UnitSerializer(unit)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        unit  = self.get_object(pk)
        serializer   = UnitSerializer(unit, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        unit = self.get_object(pk)
        unit.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)