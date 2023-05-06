from audioop import reverse
from collections import OrderedDict
import datetime
import json
from pyexpat.errors import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login as auth_login
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product
from django.contrib.auth.decorators import login_required
from .models import *


def storeH(request):
    if request.user.is_authenticated:
        user = request.user
        order, created = Order.objects.get_or_create(user = user, complete=False)
        items = order.orderitem_set.all()
        cartitems = order.get_item_total
    else:
        items = []
        order = {'get_cart_total':0, 'get_item_total':0}
        cartitems = order['get_item_total']
    products = Product.objects.all()
    context = {'products' : products,'cartitems':cartitems}    
    return render(request, 'store/storeG.html', context)

	

def cart(request):
    if request.user.is_authenticated:
        user = request.user
        order, created = Order.objects.get_or_create(user = user, complete=False)
        items = order.orderitem_set.all()
        cartitems = order.get_item_total
    else:
        items = []
        order = {'get_cart_total':0, 'get_item_total':0}
        cartitems = order['get_item_total']

    context = {'items': items , 'order':order ,'cartitems':cartitems}
    return render(request, 'store/cart.html', context)

def payment(request):
    if request.user.is_authenticated:
        user = request.user
        order, created = Order.objects.get_or_create(user = user, complete=False)
        items = order.orderitem_set.all()
        cartitems = order.get_item_total
    else:
        items = []
        order = {'get_cart_total':0, 'get_item_total':0}
        cartitems = order['get_item_total']
    
    if request.method == 'POST':
        user = request.user
        order = Order.objects.get(user=user, complete=False)
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zipcode = request.POST.get('zipcode')
        tel = request.POST.get('tel')
        shipping_address = ShippingAddress(user=request.user, order=order, address=address, city=city, state=state, pays=state, numtel=tel, codepostale=zipcode)
        shipping_address.save()
    context = {'items': items , 'order':order,'cartitems':cartitems }
    return render(request, 'store/payment.html', context) 

def login(request):
    if request.user.is_authenticated:
        return redirect('storeH')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
        
            try:
                user = User.objects.get(username=username)
            except:
                messages.error(request, 'User does not exist')
            
            user = authenticate(request, username=username, password=password)
        
            if user is not None:
                messages.success(request, 'logged in successfully!')
                auth_login(request, user)
                return redirect('storeH')
            else:
                messages.error(request, 'Incorrect password, try again')
    
    return render(request, 'store/login.html')
def signup(request):
    #form = RegisterForm()
    if request.method == 'POST' :
        form = UserCreationForm(request.POST)       
        if form.is_valid():
            print('post request')
            form.save()
            return redirect('login')
    else:    
        form = UserCreationForm()
    context = { 'form' : form}

    return render(request, 'store/signup.html', context )
	
def logout_user(request):
    logout(request)
    messages.success(request,("you logged out"))
    return redirect('storeH')  
	    
def update_item(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=400)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError as e:
        return JsonResponse({'error': 'Invalid JSON in request body'}, status=400)

    productid = data.get('productid')
    action = data.get('action')

    if not all([productid, action]):
        return JsonResponse({'error': 'Missing required parameters'}, status=400)

    user = request.user
    product = Product.objects.get(id=productid)
    order, created = Order.objects.get_or_create(user=user, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity += 1
    elif action == 'remove':
        orderItem.quantity -= 1

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse({'success': 'Item updated successfully'}, safe=False)
          
      
def processOrder(request):
    print('data:',request.body)
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    user  = request.user
    order, created = Order.objects.get_or_create(user=user, complete=False)
    order.transaction_id = transaction_id
    total = data['shipping']['total']
    if total == order.get_cart_total:
        order.complete = True  
    order.save()
 
    ShippingAddress.objects.create(
            user=user,
            order = order,
            address = data['shipping']['address'],
            city = data['shipping']['city'],
            pays = data['shipping']['pays'],
            numtel = data['shipping']['tel'],
            codepostale = data['shipping']['zipcode'],
        )     

    return JsonResponse('payment subbmitted',safe=False)
   