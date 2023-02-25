from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login, logout
# Create your views here.\


def home(request):
    seminars = Seminar.objects.all()
    context = {
        'seminars': seminars,
    }
    return render(request, 'seminar/home.html', context)


def seminardetails(request, pk_test):
    seminar = Seminar.objects.get(id=pk_test)
    user = UserInformation.objects.get(user=request.user.id)
    if request.method == 'POST':
        register = Registration(user=user, seminar=seminar)
        seminar.seat = seminar.seat-1
        register.save()
        seminar.save()

    context = {
        'seminar': seminar,
    }

    return render(request, 'seminar/seminardetails.html', context)


def signup(request):
    form = UserForm()
    print(form)
    if request.method == 'POST':
        form = UserForm(request.POST)
        form.instance.username = request.POST['email']
        if form.is_valid():
            login(request, form.save())
            UserInformation.objects.create(user=request.user)
            return redirect('home')
    context = {'form': form}
    return render(request, 'seminar/signup.html', context)


def signin(request):
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return redirect('signin')

    return render(request, 'seminar/signin.html')
