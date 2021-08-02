from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape
from django.db.models import Q
from ..models import Employee
from ..serializers import EmployeeSerializer, EmployeeEditSerializer, EmployeeReadSerializer, PasswordSerializer, EmployeeShortSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser

class EmployeeList(APIView):
    parser_classes = (MultiPartParser, FormParser)
    
    def get(self, request, format=None):
        employees     = Employee.objects.all()
        serializer    = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = EmployeeSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():

            name        = serializer.validated_data["name"]
            lastname    = serializer.validated_data["lastname"]
            code        = serializer.validated_data["code"]
            
            
            information = None
            if "information" in serializer.validated_data:
                information = serializer.validated_data["information"]
            
            address  = None
            if "address" in serializer.validated_data:
                address     = serializer.validated_data["address"]
            
            photo = None
            if "photo" in serializer.validated_data:
                photo = serializer.validated_data["photo"]
                
            user = serializer.validated_data["user"]
            
            userObj     = User.objects.filter(email=user["email"]).first()
            employeeObj = Employee.objects.filter(code=code).first()
            
            if((userObj is None) and (employeeObj is None)):
                usercreate = User.objects.create(email=user["email"], username=user["email"], is_active=user["is_active"])
                usercreate.set_password(user["password"])
                usercreate.save()
                
                if(photo is None):
                    employeeNew = Employee.objects.create(user=usercreate, code=code, name=name, lastname=lastname, address=address, information=information)
                else:
                    employeeNew = Employee.objects.create(user=usercreate, code=code, name=name, lastname=lastname, address=address, information=information, photo=photo)
                    
                serializer      = EmployeeReadSerializer(employeeNew,context={"request": request})
            else:
                return Response({"error": "Ya existe un Empleado registrado con el mismo Username y/o Código"}, status=status.HTTP_400_BAD_REQUEST)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EmployeeDetail(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAdminUser]
    
    def get_object(self, pk):
        try:
            return Employee.objects.get(pk=pk)
        except Employee.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        employee  = self.get_object(pk)
        serializer   = EmployeeSerializer(employee)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        employee       = self.get_object(pk)
        userObj        = employee.user
        serializer     = EmployeeEditSerializer(employee, data=request.data)
        if serializer.is_valid():
            #serializer.save()
            name     = serializer.validated_data["name"]
            lastname = serializer.validated_data["lastname"]
            code     = serializer.validated_data["code"] 
            
            photo = None
            if "photo" in serializer.validated_data:
                photo = serializer.validated_data["photo"]
                
            information = None
            if "information" in serializer.validated_data:
                information = serializer.validated_data["information"]
            
            address  = None
            if "address" in serializer.validated_data:
                address     = serializer.validated_data["address"]
            
            employee.name     = name
            employee.lastname = lastname
            employee.address  = address
            employee.information  = information
            
            
            if code != employee.code :
                employeeObj = Employee.objects.filter(code=code).first()
                if ((employeeObj is None)):
                    employee.code = code
                    

            if photo is not None:
                employee.photo = photo
                
            employee.save()
            
            user = serializer.validated_data["user"]
            userObj.is_active = user["is_active"]
            userObj.save()
            
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        employee = self.get_object(pk)
        employee.user.delete()
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderListEmployeeJson(BaseDatatableView):
    order_columns = ['id']

    def get_initial_queryset(self):
        return  Employee.objects.all()

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        if search:
            print(search)
            qs = qs.filter(Q(name__istartswith=search)| Q(lastname__istartswith=search) | Q(user__email__istartswith=search))

        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            
            status = item.user.is_active 
            
            statusHtml = "Inactivo"
            
            if(status):
                statusHtml = "Activo"
            
            code  = "N/A"
            if item.code:
                code = item.code
                
                
            #escape("{0}".format(item.user.email)), 
                
            
            json_data.append([
                escape("{0}".format(code)),
                escape("{0}".format(item.name)),  
                escape("{0}".format(item.lastname)), 
                statusHtml,
                '<i data-id="{0}"  class="la la-pencil-square ico-edit js-edit"></i>'.format(item.id),
                '<i data-id="{0}"class="la la-trash ico-trash js-delete"></i>'.format(item.id),
            ])
            
        return json_data



@api_view(["GET"])
def getAllEmployee(request):
    user = request.user
    employees     = Employee.objects.all().exclude(user=user)
    serializer    = EmployeeSerializer(employees, many=True, context={"request": request})
    return Response(serializer.data)



@api_view(["GET"])
def profileEmployee(request):
    user = request.user
    employeeObj = Employee.objects.filter(user=user).first()
    serializer = EmployeeReadSerializer(employeeObj, context={"request": request})
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def change_password_login(request):
    serializer = PasswordSerializer(data=request.data)
    if serializer.is_valid():
        password = serializer.validated_data["password"]
        user = request.user
        print(password)
        user.set_password(password)
        user.save()
        return Response(True)
    return Response(False)


@api_view(["POST"])
def changeProfileEmployee(request):
    serializer = EmployeeShortSerializer(data=request.data)
    
    if serializer.is_valid():
        name           = serializer.validated_data["name"]
        information    = serializer.validated_data["information"]
        lastname       = serializer.validated_data["lastname"]
        address        = serializer.validated_data["address"]
        
        user = request.user
        employeeObj = Employee.objects.filter(user=user).first()
        
        if(employeeObj is not None):
            employeeObj.name = name
            employeeObj.information = information
            employeeObj.lastname = lastname
            employeeObj.address  = address
            employeeObj.save()
            return Response(True)
    
    print(serializer.errors)
        
    return Response(False)


@api_view(["POST"])
def avatar(request):
    user = request.user
    employeeObj = Employee.objects.filter(user=user).first()
    images_data = request.FILES
    
    print(images_data['file'])
    
    #print(images_data['file'])
    if(employeeObj):
        for image_data in images_data.values():
            employeeObj.photo = images_data['file']
            employeeObj.save() 
        return Response(True)
    
    return Response(False)


@api_view(["GET"])
@permission_classes([IsAdminUser])
def employeeJson(request):
    employees = Employee.objects.all()
    json_data = []
    for employee in employees:
        json_data.append({
            "text": employee.name + " " +employee.lastname, 
            "value" : employee.id
        })
    return Response(json_data)