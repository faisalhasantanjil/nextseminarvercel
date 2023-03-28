from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login, logout
from .decorators import organization_access_only, user_access_only

from bootstrap_datepicker_plus.widgets import DateTimePickerInput
# Create your views here.\


def home(request):
    user = request.user
    print(user)
    print(user.user_permissions)
    seminars = Seminar.objects.all()
    context = {
        'seminars': seminars,
    }
    return render(request, 'seminar/home.html', context)


def seminardetails(request, pk_test):
    seminar = Seminar.objects.get(id=pk_test)
    user = UserInformation.objects.get(user=request.user.id)
    registered_seminar = Registration.objects.filter(
        user=user.id, seminar=seminar.id).first()
    print(registered_seminar)
    if request.method == 'POST':
        register = Registration(user=user, seminar=seminar)
        seminar.seat = seminar.seat-1
        register.save()
        seminar.save()
        return HttpResponseRedirect(request.path_info)

    context = {
        'seminar': seminar,
        'registered_seminar': registered_seminar,
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


def signout(request):
    logout(request)
    return redirect('signin')


@organization_access_only()
def addseminar(request):
    form = SeminarForm()
    #form.fields['start_date'].widget = DateTimePickerInput()
    if request.method == 'POST':
        form = SeminarForm(request.POST, request.FILES)
        form.instance.organization = Organization.objects.get(
            user=request.user.id)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.path_info)

    context = {
        'form': form,
    }
    return render(request, 'seminar/addseminar.html', context)


def organizedseminar(request, pk_test):
    organization = Organization.objects.get(id=request.user.id)
    pass


@user_access_only()
def myseminar(request):
    user = UserInformation.objects.get(id=request.user.id)

    seminars = Registration.objects.filter(user=request.user.id)
    for i in seminars:
        print(i.seminar.id)
    context = {
        'seminars': seminars,
    }
    return render(request, 'seminar/myseminar.html', context)
