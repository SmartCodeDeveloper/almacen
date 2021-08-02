import os
import requests
import json
from api.models import Order, Notification, Inventory, DetailInventory, Product, Employee
from django.db.models import Sum, F


def cron_notificaciones():
    orders    = Order.objects.filter(torder=1, status=1)
    products  = Product.objects.filter(minstock__gt=F('stock')).order_by('id')
    
    message = ""
    for orde in orders:
        if(orde.employee):
            message = "Tiene una solicitud de Pedido Nro {0} que esta pendiente por procesar de, del Cliente:  {1} {2}".format(orde.pk, orde.employee.name, orde.employee.lastname)
            Notification.objects.create(message=message, read=False)
    
    message = ""
    for prod in products:
        message = message + " {0} - {1} esta por debajo del stock mínimo , ".format(prod.code, prod.name)
    
    if(message!=""):
        message = "Productos de Bajo Stock en el Almacén Principal: " + message
        Notification.objects.create(message=message, read=False)
    
    employees = Employee.objects.all() 
    for emp in employees:
        message = ""
        invObj  = Inventory.objects.filter(employee=emp).first()
        if  invObj:
            message = ""
            details = DetailInventory.objects.filter(inventory=invObj)
            for det in details:
                productObj = det.product
                if(det.quantity<productObj.minstockclient):
                    message = message + " {0} - {1} esta por debajo del stock mínimo , ".format(productObj.code, productObj.name)
            
            if(message!=""):
                message = "Productos de Bajo Stock para el Cliente ({0} {1}):  ".format(emp.name, emp.lastname) + message
                Notification.objects.create(message=message, read=False)
                
    return "OK"