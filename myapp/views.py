from django.shortcuts import render,redirect
from django.http import HttpResponse
from . models import Product,Order,Customer
from .filters import OrderFilter
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import OrderForm, CreateUserForm



def base(request):
    h2 = 'This is home page'
    context = {'h2':h2}
    return render(request, 'base.html',context)


@login_required(login_url='login')
def dashboard(request):
    orders        = Order.objects.all()
    customers     = Customer.objects.all()

    total_orders  = orders.count()
    pending       = Order.objects.filter(status='Pending').count()
    delivered     = Order.objects.filter(status='Delivered').count()

    context       = {
        'orders': orders,
        'customers': customers,
        'total_orders':total_orders,
        'pending':pending,
        'delivered':delivered,


    }
    return render(request, 'accounts/dashboard.html',context)

@login_required(login_url='login')
def product(request):
    product = Product.objects.all()
    context = {'products':product}
    return render(request, 'accounts/products.html',context)


@login_required(login_url='login')
def customer(request,id):
    customer = Customer.objects.get(id=id)

    orders = customer.order_set.all()

    orderFilter = OrderFilter(request.GET, queryset=orders)

    orders = orderFilter.qs

    context = {'customer':customer,'orders':orders,'orderFilter':orderFilter,}
    return render(request, 'accounts/customer.html',context)


@login_required(login_url='login')
def createOrder(request):
    form = OrderForm()

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')

    context = {'form':form}
    return render(request, 'accounts/order_create.html',context)

@login_required(login_url='login')
def updateOrder(request, id):
    order = Order.objects.get(id=id)
    form = OrderForm(instance=order)

    if request.method == "POST":
        form = OrderForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect('dashboard')

    context = {'form':form}

    return render(request, 'accounts/order_create.html',context)

@login_required(login_url='login')
def deleteOrder(request,id):
    order = Order.objects.get(id=id)
    if request.method == "POST":
        order.delete()
        return redirect('dashboard')
    context = {'item':order}
    return render(request, 'accounts/delete.html',context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.info(request, 'Username or Password is incorrect!')
            
        context = {}
        return render(request, 'auth/login.html', context)


def signUpPage(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        form = CreateUserForm()
        if request.method == "POST":
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'User is created for '+user)
                return redirect('login')
        context = {'form':form}
        return render(request, 'auth/signup.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')



