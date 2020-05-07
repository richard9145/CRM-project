from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.forms import inlineformset_factory
from .forms import OrderForm, CreateUserForm, CreateCustomer, CustomerForm
from .filters import OrderFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .decorators import unauthenticated_user, allowed_users, admin_only

# Create your views here.

def register(request):
	if request.user.is_authenticated:
		return redirect('medical:home')

	else:
		form = CreateUserForm()
		if request.method =='POST':
			form = CreateUserForm(request.POST)
			if form.is_valid():
				user = form.save()
				username = form.cleaned_data.get('username')

				# This was commented out because it worked better with signals.py
				# group = Group.objects.get(name='customer')
				# user.groups.add(group)

				# Customer.objects.create(
				# 	user=user,
				# 	name=user.username,
				# 	)

				messages.success(request, 'Account for '+ username + ' was created successfully')
				return redirect('medical:login')

		context = {'form': form}
		return render(request, 'medical/register.html', context)



@unauthenticated_user
def loginPage(request):
	
	if request.method == 'POST':
		username= request.POST.get('username')
		password= request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('medical:home')
		else:
			messages.info(request, 'Username or Password is not correct')

	context= {}
	return render(request, 'medical/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('medical:login')


@login_required(login_url='medical:login')
@admin_only
def home(request):
	customers = Customer.objects.all()
	orders = Order.objects.all()

	total_customer = customers.count()

	total_order = orders.count()
	delivered = orders.filter(status='Delivered').count()
	pending = orders.filter(status='Pending').count()


	context = { 'customers': customers, 'orders': orders, 'total_order': total_order, 'delivered': delivered, 'pending': pending}

	return render(request, 'medical/dashboard.html', context)


@login_required(login_url='medical:login')
@allowed_users(allowed_roles=['admin'])
def products(request):
	products = Product.objects.all()
	return render(request, 'medical/products.html', {'products': products})


@login_required(login_url='medical:login')
@allowed_users(allowed_roles=['admin'])
def customer(request, cust):
	customer = Customer.objects.get(id=cust)
	orders = customer.order_set.all()
	orders_count = orders.count()

	#this handle the search bar on the customer page
	myFilter = OrderFilter(request.GET, queryset=orders)
	orders = myFilter.qs

	context = {'customer': customer, 'orders': orders, 'orders_count': orders_count, 'myFilter': myFilter}
	return render(request, 'medical/customer.html', context)


@login_required(login_url='medical:login')
@allowed_users(allowed_roles=['admin'])
def CustomerCreation(request):
	create_cust = CreateCustomer()

	if request.method == 'POST':
		create_cust = CreateCustomer(request.POST)
		if create_cust.is_valid():
			create_cust.save()
			return redirect ('/')
	
	context = {'create_cust': create_cust}

	return render(request, 'medical/createcust.html', context)


@login_required(login_url='medical:login')
@allowed_users(allowed_roles=['admin'])
def CreateOrder(request, co):
	OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=5)
	customer = Customer.objects.get(id=co)
	formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
	# form = OrderForm({'customer':customer})
	if request.method == 'POST':
		# form = OrderForm(request.POST)
		formset = OrderFormSet(request.POST, instance=customer)
		if formset.is_valid():
			formset.save()
			return redirect('/')

	context = {'formset':formset}
	return render(request, 'medical/order_form.html', context)



@login_required(login_url='medical:login')
@allowed_users(allowed_roles=['admin'])
def UpdateOrder(request, uf):
	order = Order.objects.get(id=uf)
	form = OrderForm(instance=order)
	if request.method == 'POST':
		form = OrderForm(request.POST, instance=order)
		if form.is_valid():
			form.save()
			return redirect('/')
	
	context = {'form':form}
	return render(request, 'medical/update_form.html', context)



@login_required(login_url='medical:login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, do):

	order = Order.objects.get(id=do)
	if request.method == 'POST':
		order.delete()
		return redirect('/')
	context= {'item': order}
	return render(request, 'medical/delete_order.html', context)


@login_required(login_url='medical:login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
	orders = request.user.customer.order_set.all()

	total_order = orders.count()
	delivered = orders.filter(status='Delivered').count()
	pending = orders.filter(status='Pending').count()

	context = {'orders':orders, 'total_order': total_order, 'delivered': delivered, 'pending': pending}
	return render(request, 'medical/user.html', context)


@login_required(login_url='medical:login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):

	customer = request.user.customer
	form = CustomerForm(instance=customer)

	if request.method == 'POST':
		form = CustomerForm(request.POST, request.FILES, instance=customer)
		if form.is_valid():
			form.save()
	
	context = {'form': form}
	return render(request, 'medical/account_settings.html', context)