import email
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import inlineformset_factory
from accounts.models import *
from accounts.forms import *
from accounts.filters import *
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm,authenticate
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='login')

def dashboard(request):
    all_customers = Customer.objects.all()
    current_user = request.user
    all_orders = Order.objects.all()
    total_orders = Order.objects.all().count()
    delivered_orders = Order.objects.filter(status__icontains="Delivered").count()
    pending_orders = Order.objects.filter(status="Pending").count()
    
    Context = {"customers":all_customers,
               "orders":all_orders,
               "total_orders":total_orders,
               "delivered_orders":delivered_orders,
               "pending_orders":pending_orders,
               'user':current_user}

    return render(request, 'accounts/dashboard.html',context=Context)

@login_required(login_url='login')
def product(request):
    products = Product.objects.all()
    tag = Tag.objects.all()
    context = {"Products":products,"Tag":tag}
    
    return render(request, 'accounts/product.html',context)

@login_required(login_url='login')
def customer(request,pkey):
    certain_customer = Customer.objects.get(id=pkey)
    customer_orders = certain_customer.order_set.all()
    total_orders = certain_customer.order_set.all().count


    orderfilter = OrderFilter(request.GET,queryset=customer_orders)
    customer_orders = orderfilter.qs
    Context = {"certain_customer":certain_customer,"customer_orders":customer_orders,
               "total_orders":total_orders,'OrderFilter':orderfilter}
               
    
    return render(request, 'accounts/customer.html',context=Context)

@login_required(login_url='login')
def all_customers(request):
    all_customers = Customer.objects.all()
    context = {"customers":all_customers}
    return render(request,'accounts/all_customers.html',context)

@login_required(login_url='login')
def CreateCustomer(request):

    form = CustomerForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('/')
    context = {"form":form}
    return render(request,'accounts/create_customer.html',context=context)

@login_required(login_url='login')
def CreateOrder(request,pk):
    customer_id = Customer.objects.get(id=pk)
    OrderFormSet = inlineformset_factory(Customer,Order,fields=('product','status')
                                         ,extra=5)
    formset = OrderFormSet(queryset=Order.objects.none(),instance=customer_id)
    if request.method=="POST":
        formset = OrderFormSet(request.POST,instance=customer_id)
        if formset.is_valid():
          formset.save()
          return redirect('/')
    context = {"formset":formset,"customer":customer_id}
    return render(request,'accounts/create_order.html',context)

@login_required(login_url='login')
def DeleteOrder(request,pk):
  order_id = Order.objects.get(id=pk)
  if request.method=="POST":
      order_id.delete()
      return redirect('/')
  context = {"item":order_id}
  return render(request,'accounts/delete_order.html',context)

@login_required(login_url='login')
def DeleteCustomer(request,pk):
    customer = Customer.objects.get(id=pk)
    if request.method=="POST":
        customer.delete()
        return redirect('/')
    context = {"customer":customer}
    return render(request,'accounts/delete_customer.html',context)
    
@login_required(login_url='login')
def UpdateCustomer(request,pk):
    customer_data = Customer.objects.get(id=pk)
    form = CustomerForm(instance=customer_data)
    if request.method=='POST':
        form = CustomerForm(request.POST,instance=customer_data)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {"customer":customer_data,'form':form}

    return render(request,'accounts/update_customer.html',context)

@login_required(login_url='login')
def UpdateOrder(request,pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method=="POST":
        form = OrderForm(request.POST,instance = order)
        if form.is_valid():
          form.save()
          return redirect('/')
    
    context = {"form":form,'order':order}
    return render(request,'accounts/update_order.html',context)

def registerpage(request):
    form = CreateUserForm()
    if request.method=="POST":
        form = CreateUserForm(request.POST)
        user_objects = User.objects.all()
        usernames = [user.username for user in user_objects]
        if request.POST.get('username') in usernames:
            messages.error(request,'Username already exists')
        elif form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request,'Account was created for ' + user)
            return redirect('login')
        else:
            messages.error(request,'Invalid details')
            return redirect('register')

    context = {'form':form}
    return render(request,'accounts/register.html',context)

def loginpage(request):
    if request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Incorrect username or password')
        
    return render(request,'accounts/login.html')

def logoutpage(request):
    logout(request)
    if request.user is None:
        pass
        return redirect('/')
    return redirect('login')

@login_required(login_url='login')
def forgotpassword(request,user_id):
    
    user = User.objects.get(id=user_id)
    
    form = ForgotpasswordForm(initial=user)
    
    if form.is_valid():
        form.save()
        messages.success(request,'Password changed Successfully!')
        return redirect('/')

    context={'user':user,'form':form}
    return render(request,'accounts/forgotpwdform.html',context)