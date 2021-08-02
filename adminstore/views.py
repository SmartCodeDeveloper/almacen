from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from api.models import Brand, Unit, Employee, Order, DetailOrder, Category, Manifest, DetailManifest, Product, Notification, Inventory, DetailInventory
from django.http import HttpResponseRedirect, HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from django.utils.html import strip_tags
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from adminstore.tokens import account_activation_token
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.models import User
import os
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django.db.models import Sum, F
import pandas as pd
from io import BytesIO as IO
import json 




# Create your views here.


@login_required(login_url='/login')
def notificaciones(request):
    gname = request.user.groups.all()[0].name

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
                
    return render(request, "report/notificaciones.html", {"gname": gname})

def sendemail(titulo, mensaje, usuario):
    subject = titulo
    message = mensaje
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [usuario,]
    send_mail( subject, strip_tags(message), email_from, recipient_list, html_message=mensaje )
    return "si"


@login_required(login_url='/login')
def showmanifest(request, manifest):
    gname = request.user.groups.all()[0].name
    manifestObj = Manifest.objects.get(pk=manifest)
    details     = DetailManifest.objects.filter(manifest=manifestObj)
    for deta in details:
        productObj = deta.product 
        categories = productObj.categories.all()
        catNames   = ""
        
        for category in categories:
            catNames = category.code+" "+category.name+", "
            
        deta.catNames = catNames
    return render(request, "manifest/show-manifest.html", {"manifest":  manifestObj, "details": details, "gname": gname})


@login_required(login_url='/login')
def listnotificaciones(request):
    gname = request.user.groups.all()[0].name
    Notification.objects.all().update(read=True)
    return render(request, "report/notificaciones.html",{"gname": gname})


@login_required(login_url='/login')
def manifest(request):
    gname = request.user.groups.all()[0].name
    employees = Employee.objects.all()
    return render(request, "manifest/manifest.html", {"employees": employees, "gname": gname})


@login_required(login_url='/login')
def manifestorder(request, order):
    gname = request.user.groups.all()[0].name
    employees    = Employee.objects.all()
    orderObj     = Order.objects.get(pk=order)
    details      = DetailOrder.objects.filter(order=orderObj)
    manifestObj  = Manifest.objects.filter(order=orderObj).first()
    
    
    for deta in details:
        productObj = deta.product 
        categories = productObj.categories.all()
        catNames   = ""
        
        for category in categories:
            catNames = category.code+" "+category.name+", "
        
            
        deta.catNames = catNames
        
        initialValues = []
        
        seriales      = deta.seriales 
        if seriales!=None:
            seriales      = seriales.split(",")
            for ser in seriales:
                initialValues.append({"text": ser, "value" : ser})
        
        deta.initialValues = json.dumps(initialValues, indent = 4)
            
    
    if manifestObj:
        detailsManifest     = DetailManifest.objects.filter(manifest=manifestObj)
        
        for deta in detailsManifest:
            productObj = deta.product 
            categories = productObj.categories.all()
            catNames   = ""
            
            for category in categories:
                catNames = category.code+" "+category.name+", "
            
                
            deta.catNames = catNames
            
            initialValues = []
            seriales      = deta.seriales 
            if seriales!=None:
                seriales      = seriales.split(",")
                for ser in seriales:
                    initialValues.append({"text": ser, "value" : ser})
            
            deta.initialValues = json.dumps(initialValues, indent = 4)
        
        
        return render(request, "manifest/show-manifest.html", {"manifest":  manifestObj, "details": detailsManifest, "gname": gname})
    
    return render(request, "manifest/manifest-order.html", {"employees": employees, "order": orderObj, "details": details, "gname": gname })

@login_required(login_url='/login')
def listmanifest(request):
    gname = request.user.groups.all()[0].name
    return render(request, "manifest/list.html",{"gname": gname})


@login_required(login_url='/login')
def listtransfer(request):
    gname = request.user.groups.all()[0].name
    return render(request, "transfer/list.html", {"gname": gname})

@login_required(login_url='/login')
def category(request, category):
    gname = request.user.groups.all()[0].name
    return render(request, "category/list.html", {"category": category, "gname": gname})

@login_required(login_url='/login')
def employee(request):
    gname = request.user.groups.all()[0].name
    return render(request, "employee/list.html",{"gname": gname})

@login_required(login_url='/login')
def brand(request):
    gname = request.user.groups.all()[0].name
    return render(request, "brand/list.html", {"gname": gname})

@login_required(login_url='/login')
def product(request):
    gname = request.user.groups.all()[0].name
    brands = Brand.objects.all()
    units  = Unit.objects.all()
    return render(request, "product/list.html", {"brands": brands, "units": units, "gname": gname })

@login_required(login_url='/login')
def product_category(request, category):
    gname = request.user.groups.all()[0].name
    brands   = Brand.objects.all()
    units    = Unit.objects.all()
    categoryObj = Category.objects.get(pk=category)
    return render(request, "product/list-product-category.html", {"brands": brands, "units": units, "category": categoryObj, "gname": gname })

@login_required(login_url='/login')
def order(request):
    gname = request.user.groups.all()[0].name
    employees = Employee.objects.all()
    return render(request, "order/order-form.html", { "employees": employees, "gname": gname })

@login_required(login_url='/login')
def orderEdit(request, order):
    gname = request.user.groups.all()[0].name
    order = Order.objects.get(pk=order)
    details = DetailOrder.objects.filter(order=order)
    for deta in details:
        productObj = deta.product 
        categories = productObj.categories.all()
        catNames   = ""
        for category in categories:
            catNames = category.code+" "+category.name+", "
        deta.catNames = catNames
        initialValues = []
        seriales      = deta.seriales 
        if seriales!=None:
            seriales      = seriales.split(",")
            for ser in seriales:
                initialValues.append({"text": ser, "value" : ser})
        
        deta.initialValues = json.dumps(initialValues, indent = 4)
         
        
    employees = Employee.objects.all()
    return render(request, "order/order-form-edit.html", { "order": order, "details": details, "employees": employees, "gname": gname })

@login_required(login_url='/login')
def listorder(request):
    gname = request.user.groups.all()[0].name
    orders = Order.objects.all().order_by('-pk')
    return render(request, "order/list.html", { "orders": orders, "gname": gname })

def recovery(request):
    gname = request.user.groups.all()[0].name
    return render(request, "login/recovery.html", {"gname": gname})

@login_required(login_url='/login')
def changePassword(request):
    gname = request.user.groups.all()[0].name
    user = request.user
    if(request.method=="POST"):
        password = request.POST.get("password")
        user.set_password(password)
        user.save()
        return render(request, "profile/profilepassword.html", { "mjs": "Password Actualizado Exitosamente", "gname": gname })
    return render(request, "profile/profilepassword.html",{"gname": gname})

@login_required(login_url='/login')
def profile(request):
    gname = request.user.groups.all()[0].name
    user = request.user
    if(request.method=="POST"):
        name      = request.POST.get("name")
        lastname  = request.POST.get("lastname")
        
        user.first_name = name 
        user.last_name  = lastname
        
        user.save()
        
        return render(request, "profile/profile.html", { "mjs": "Perfil Actualizado Exitosamente", "gname": gname })
        
    return render(request, "profile/profile.html", {"gname": gname})

@login_required(login_url='/login')
def dashboard(request):
    gname = request.user.groups.all()[0].name
    orders   = Order.objects.all().order_by('-id')[:5]
    total    = Order.objects.all().count()
    pending  = Order.objects.filter(status=1).count()
    approved = Order.objects.filter(status=2).count()
    denied   = Order.objects.filter(status=3).count()
    return render(request, "dashboard/dashboard.html", { "orders": orders, "total": total, "pending": pending, "approved": approved, "denied": denied,"gname": gname})

@login_required(login_url='/login')
def logout_system(request):
    logout(request)
    return redirect('/login')

@login_required(login_url='/login')
def report_inventory(request):
    gname = request.user.groups.all()[0].name
    return render(request, "report/stock.html",{"gname": gname})


@login_required(login_url='/login')
def report_inventory_principal(request):
    gname = request.user.groups.all()[0].name
    products = Product.objects.all()
    return render(request, "report/stockprincipal.html", {"products": products, "gname": gname})

@login_required(login_url='/login')
def report_inventory_principal_filter(request):
    gname = request.user.groups.all()[0].name
    data = request.GET['category']
    catid = data.split(',')
    print(len(catid))
    clen = len(catid)
    query = 'select * from (select * FROM (select new_tb.product_id , count(new_tb.product_id) as product_total FROM (select * FROM api_product_categories where category_id IN({})) AS new_tb Group BY new_tb.product_id) as sec_db WHERE sec_db.product_total >= {} ORDER BY product_id ASC) as thir_db, api_product where api_product.id=thir_db.product_id'
    query = query.format(data,clen)
    print(query) 
    if data:
        products = Product.objects.raw(query)
    else:
        products = Product.objects.all()
    return render(request, "report/stockprincipal.html", {"products": products, "gname": gname})

@login_required(login_url='/login')
def report_excel_stock_principal(request):
    
    excel_file = IO()
    
    
    products = Product.objects.all()
    codes    = []
    names    = []
    stocks    = []
    for prod in products:
        codes.append(prod.code)
        names.append(prod.name)
        stocks.append(prod.stock)
    
    
    
    # Create a Pandas dataframe from some data.
    df = pd.DataFrame({'codigo': codes, 'nombre': names, 'stocks': stocks})
    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter(excel_file, engine='xlsxwriter')
    # Convert the dataframe to an XlsxWriter Excel object.
    df.to_excel(writer, sheet_name='Sheet1')
    
    # Close the Pandas Excel writer and output the Excel file.
    writer.save()
    
    excel_file.seek(0)
    
    response = HttpResponse(excel_file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="excel_stock.xlsx"'
    
    return response



@login_required(login_url='/login')
def report_mov(request):
    gname = request.user.groups.all()[0].name
    return render(request, "report/mov.html",{"gname": gname})

@login_required(login_url='/login')
def report_bestseller(request):
    gname = request.user.groups.all()[0].name
    products = Product.objects.all()
    
    for p in products:
        detail = DetailOrder.objects.filter(product=p, order__torder=1).aggregate(quantity_sum=Sum('quantity'))

        if detail['quantity_sum'] :
            p.sum = detail['quantity_sum']
        else:
            p.sum = 0
    
    productsnew = sorted(products, key=lambda x: x.sum, reverse=True)
    productsnew = productsnew[0:30]
    
    print(productsnew)
    
    return render(request, "report/items.html", {"products": productsnew, "gname": gname})


@login_required(login_url='/login')
def report_excel_best_seller(request):
    
    excel_file = IO()
    
    products = Product.objects.all()
    
    for p in products:
        detail = DetailOrder.objects.filter(product=p, order__torder=1).aggregate(quantity_sum=Sum('quantity'))

        if detail['quantity_sum'] :
            p.sum = detail['quantity_sum']
        else:
            p.sum = 0
    
    productsnew = sorted(products, key=lambda x: x.sum, reverse=True)
    productsnew = productsnew[0:30]
    
    codes    = []
    names    = []
    cantidad    = []
    for prod in productsnew:
        codes.append(prod.code)
        names.append(prod.name)
        cantidad.append(prod.sum)
    
    
    
    # Create a Pandas dataframe from some data.
    df = pd.DataFrame({'codigo': codes, 'nombre': names, 'cantidad': cantidad})
    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter(excel_file, engine='xlsxwriter')
    # Convert the dataframe to an XlsxWriter Excel object.
    df.to_excel(writer, sheet_name='Sheet1')
    
    # Close the Pandas Excel writer and output the Excel file.
    writer.save()
    
    excel_file.seek(0)
    
    response = HttpResponse(excel_file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="excel_low_stock.xlsx"'
    
    return response



@login_required(login_url='/login')
def reportlowstock(request):
    gname = request.user.groups.all()[0].name
    products = Product.objects.filter(minstock__gte=F('stock')).order_by('id')
    return render(request, "report/low.html", {"products": products, "gname": gname})



@login_required(login_url='/login')
def report_excel_low_stock(request):
    
    excel_file = IO()
    
    products = Product.objects.filter(minstock__gte=F('stock')).order_by('id')
    codes    = []
    names    = []
    stocks    = []
    for prod in products:
        codes.append(prod.code)
        names.append(prod.name)
        stocks.append(prod.stock)
    
    
    
    # Create a Pandas dataframe from some data.
    df = pd.DataFrame({'codigo': codes, 'nombre': names, 'cantidad': stocks})
    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter(excel_file, engine='xlsxwriter')
    # Convert the dataframe to an XlsxWriter Excel object.
    df.to_excel(writer, sheet_name='Sheet1')
    
    # Close the Pandas Excel writer and output the Excel file.
    writer.save()
    
    excel_file.seek(0)
    
    response = HttpResponse(excel_file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="excel_low_stock.xlsx"'
    
    return response

def login_system(request):
    if(request.method == "POST"):
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(username)
        print(password)
        user     =  authenticate(username=username, password=password)
        print(user)

        if user and user.is_superuser:
            #if user.is_active:
            login(request, user)
            return redirect('/')
                #return HttpResponseRedirect(reverse('home'))
        return render(request, 'login/login.html', {"msj": "usuario y/o contraseña incorrectos"})
    else:
        return render(request, 'login/login.html')


@csrf_exempt
@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def forgot(request):
    email = request.data['email']
    userForgot  = User.objects.filter(username=email).first()
    print(userForgot)
    if userForgot:
        try:
            current_site = get_current_site(request)
            sendemail('Ha olvidado su password, Restaurar', render_to_string('login/forgotpassword.html', {'user': userForgot,	'domain': current_site.domain,	'uid':urlsafe_base64_encode(force_bytes(userForgot.pk)), 'token':account_activation_token.make_token(userForgot), }), email)
            return Response(True)
        except Exception as e:
            #print(e.message)
            print(e)

    return Response(False)

def reset_password(request, uidb64, token):

    error   = "si"
    mensaje ="no"

    if request.method == "POST":

        password = request.POST.get("password")
        mensaje  = "Error al cambiar la contraseña, vuelva a intentar"
        print(password)

        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            userPass = User.objects.get(pk=uid)
            print(userPass)
            print("llego")
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        
        if userPass is not None and account_activation_token.check_token(userPass, token):
            #user.is_active = True
            #user.save()
            userPass.set_password(password)
            userPass.save()
            mensaje = "Contraseña cambiada exitósamente"
            error   = "no"

            return render(request, 'login/formforgotpassword.html', {'error': error, 'mensaje':mensaje})

    return render(request, 'login/formforgotpassword.html', {'error': error, 'mensaje': mensaje})



@login_required(login_url='/login')
def load_csv(request):
    gname = request.user.groups.all()[0].name
    if request.method == "POST" and request.FILES:
        print("csvss")
        print(request.FILES['csv'])
        print("abajo de request files")
        csv  = request.FILES['csv']
        data = pd.read_csv(csv)
        print(data)
        print(data.head())
        
        data = data.astype(str)
        
        user = request.user
        
        for index, row in data.iterrows():
            print(row)
            name           = row["nombre"]
            serie          = row["serie"]
            series         = row["series"]
            code           = row["codigo"]
            brand          = row["marca"]
            categories     = row["categorias"]
            unit           = row["unidad"]
            stock          = row["stock"]
            minstockclient = row["stockminimocliente"]
            minstock       = row["stockminimoalmacen"]
            activo         = row["activo"]
            price          = row["precio"]
            brandObj       = None
            unitObj        = None
            photo          = None
            
            
            if brand=="nan":
                brand = None
            else:
                brandObj = Brand.objects.get(pk=brand)
            
            if unit=="nan":
                unit  = None
            else:
                unitObj = Unit.objects.filter(name=unit).first()
            
            
            print("=======")
            print(categories)
            print("*********")
            
            if categories=="nan":
                categories = None
            else:
                categories = categories.split("-")
            
            print("==============")
            print(categories)
            print("*************")
            
            if serie=="nan":
                serie  = None
            
            
            if series=="nan":
                series = None
            else:
                series = series.split("-")
                series = ",".join(series)
            
            active  = True
            
            if activo == "nan":
                active = True
            elif activo == "no":
                active = False
            else:
                active = True
            
            
            productFind = Product.objects.filter(code=code).first()
            
            if((productFind is None)):
                
                productNew    = Product.objects.create(name=name, code=code, price=price, brand=brandObj, unit=unitObj, active=active, photo=photo, stock=stock, serie=serie,  minstock=minstock, minstockclient=minstockclient, series=series)
                categoriesAdd = productNew.categories.all()
                
                for catAdd in categoriesAdd:
                    productNew.categories.remove(catAdd);
                
                print(categories)
                
                if categories is not None:
                    for category in categories:
                        categoryObj = Category.objects.filter(code=category).first()
                        if categoryObj:
                            productNew.categories.add(categoryObj);

                                
        return render(request, "product/cargar.html", {"mjs": "Se han cargado los empleados correctamente","gname": gname})

    return render(request, "product/cargar.html",{"gname": gname})


def handler404(request, exception):
    return render(request, '404.html', status=404)

def handler500(request):
    return render(request, '500.html', status=500)

