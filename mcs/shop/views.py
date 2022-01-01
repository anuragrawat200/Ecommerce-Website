from django.shortcuts import render,redirect,HttpResponse,Http404
# from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from .models import *  # Product, Contact, Orders,OrderUpdate
from math import ceil
from django.contrib.auth  import authenticate,  login, logout
import json

# importing twilio
from twilio.rest import Client



# Create your views here.
# def index(request):
#     products = Product.objects.all()
#     print(products)
#     n = len(products)
#     nSlides = n // 4 + ceil((n / 4) - (n // 4))
#     params = {'no_of_slides': nSlides, 'range': range(1, nSlides), 'product': products}
#     return render(request, 'shop/index.html', params)

def searchMatch(query, item):
    '''return true only if query matches the item'''
    if query.lower() in item.desc.lower() or query.lower() in item.p_name.lower() or query.lower() in item.category.lower():
        return True
    else:
        return False

def search(request):
    # print("kala")
    query = request.GET.get('search')
    # print(query)
    if len(query) < 4:
        messages.warning(request, "query too small")
        return redirect('ShopHome')
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query, item)]

        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod) != 0:
            allProds.append([prod, range(1, nSlides), nSlides])


    if len(allProds) == 0:
        messages.warning(request,"no matching records")
        #params = {'msg': "Please make sure to enter relevant search query"}
    params = {'allProds': allProds}
    return render(request, 'shop/search.html', params)





def index(request):
    if request.method == "POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        messages.success(request,"contact has been succesfully saved")
        contact.save()

    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(0, nSlides), nSlides])
    params = {'allProds': allProds}
    return render(request, 'shop/index.html', params)


def about(request):
    messages.warning(request,"hello about")
    return HttpResponse("<h1> hello there</h1>")
    return render(request, 'shop/about.html')




def demo(request,myid):
    #query = request.GET.get('categorypro')
    #query='Electronics'
    prod = Product.objects.filter(category=myid)
    print(prod)
    params = {'prod': prod}
    messages.success(request, "your results")
    return render(request, 'shop/index1.html', params)









# def contact(request):           # is on the index function intergrated with it
#     if request.method == "POST":
#         name = request.POST.get('name', '')
#         email = request.POST.get('email', '')
#         phone = request.POST.get('phone', '')
#         desc = request.POST.get('desc', '')
#         contact = Contact(name=name, email=email, phone=phone, desc=desc)
#         contact.save()
#     return render(request, 'shop/index.html')


def tracker(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            orderid = request.POST.get('formorderid', '')
            email = request.POST.get('formemail', '')  # inside get() name of the given form comes if using html form for post request
            print(f"{orderid} and {email}")               # and if using ajax then name is given in data in ajax like formemail here
            try:
                order = Orders.objects.filter(order_id=orderid, email=email)
                # print("hello nice")
                # print(order)
                if len(order) > 0:
                    update = OrderUpdate.objects.filter(order_id=orderid)
                    updates = []
                    for item in update:
                        updates.append({'text': item.update_desc, 'time': item.timestamp})
                        response = json.dumps(updates, default=str)
                    return HttpResponse(response)
                else:
                    return HttpResponse('{}')
            except Exception as e:
                return HttpResponse('{}')

        return render(request, 'shop/tracker.html')
    else:
        messages.warning(request,"Please login first")
        return redirect('ShopHome')






def productview(request, myid):
    product = Product.objects.filter(id=myid)
    #print(type(product))
    return render(request, "shop/prodview.html", {'product': product[0]})


def checkout(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            items_json = request.POST.get('itemsJson', '')
            name = request.POST.get('name', '')
            email = request.POST.get('email', '')
            address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
            city = request.POST.get('city', '')
            state = request.POST.get('state', '')
            zip_code = request.POST.get('zip_code', '')
            phone = request.POST.get('phone', '')

            order = Orders(items_json=items_json, name=name, email=email, address=address, city=city, state=state,
                           zip_code=zip_code, phone=phone)
            order.save()
            update = OrderUpdate(order_id=order.order_id, update_desc="your order has been placed")
            update.save()
            thank = True
            id = order.order_id

            # # Your Account Sid and Auth Token from twilio.com / console
            # account_sid = 'AC33bb768eca93a3bdf6473b5a777968ba'
            # auth_token = '0fd819bf7620c182b1f87beccd56f9e9'
            #
            # client = Client(account_sid, auth_token)
            #
            # ''' Change the value of 'from' with the number
            # received from Twilio and the value of 'to'
            # with the number in which you want to send message.'''
            # message = client.messages.create(
            #     from_='+19096396588',
            #     body='Your order has been placed with order id ' + str(id) ,
            #     to=phone
            # )
            return render(request, 'shop/checkout.html', {'thank': thank, 'id': id})
        return render(request, 'shop/checkout.html')
    else:
        messages.warning(request,"Please login first")
        return redirect('ShopHome')





def handleSignUp(request):
    if request.method == "POST":
        # Get the post parameters
        username = request.POST['username']
        email = request.POST['email1']
        fname = request.POST['fname']
        lname = request.POST['lname']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        # check for errorneous input

        check=User.objects.filter(username=username)
        if len(check) > 0:
            messages.warning(request, " Username already exists")
            return redirect('ShopHome')

        check = User.objects.filter(email=email)
        if len(check) > 0:
            messages.warning(request, " Account with this email is already exists please provide another")
            return redirect('ShopHome')

        if len(username) > 10:
            messages.warning(request, " Your user name must be under 10 characters")
            return redirect('ShopHome')

        if not username.isalnum():
            messages.warning(request, " User name should only contain letters and numbers")
            return redirect('ShopHome')


        if (len(pass1)<6 or pass1 != pass2):
            messages.warning(request, " Either Password length is not at least 7 or Passwords do not match Please check")
            return redirect('ShopHome')


        # check for errorneous input

        # Create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()


        messages.success(request, " Your account has been successfully created")
        return redirect('ShopHome')

    else:
        return HttpResponse("404 - Not found")


def handelLogin(request):
    if request.method == "POST":
        # Get the post parameters
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']
        user = authenticate(username=loginusername, password=loginpassword)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect("ShopHome")
        else:
            messages.error(request, "Invalid credentials! Please try again")
            return redirect("ShopHome")

    else:
        messages.warning(request,"please give your credentials first in login")
        return redirect("ShopHome")


def handelLogout(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Successfully logged out")
        return redirect('ShopHome')
    else:
        messages.warning(request,"Please login first")
        return redirect('ShopHome')

def handleorders(request):
    if request.user.is_authenticated:
        orders=Orders.objects.values().filter(email=request.user.email)
        print(orders)

        return render(request, 'shop/orders.html', {'orders':orders})

    else:
        messages.warning(request,"please login first")
        return redirect('ShopHome')

