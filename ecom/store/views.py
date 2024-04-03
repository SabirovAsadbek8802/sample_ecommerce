from django.shortcuts import render, redirect
from .models import Product, Category
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .forms import SignUpForm

@login_required(login_url='/login/')
def category(request, foo):
    foo = foo.replace('-', ' ')
    try:
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products': products, 'category': category})
    except:
        messages.success(request, 'Category with this name does not exist!!!')
        return redirect('home')


@login_required(login_url='/login/')
def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product': product})

@login_required(login_url='/login/')
def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})


@login_required(login_url='/login/')
def about(request):
    return render(request, 'about.html', {})


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You are now logged in!!!')
            return redirect('home')
        else:
            messages.success(request, "Invalid username or password!!!")
            return redirect('login')
    else:
        return render(request, 'login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, "You have successfully logged out!!!")
    return redirect('login')


def register_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request,'You have successfully registered!!!')
            return redirect('home')
        else:
            messages.success(request, "Invalid username or password!!!")
            return redirect('register')
    else:
        return render(request, 'register.html', {'form': form})