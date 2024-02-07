from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
import time
from django.shortcuts import get_object_or_404

from django.conf import settings
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login, logout
from .decorators import organization_access_only, user_access_only, is_organization, is_user
from django.contrib.auth.decorators import login_required

from django.core.mail import send_mail

from bootstrap_datepicker_plus.widgets import DateTimePickerInput
# Create your views here.\


# Signup for Users
def signup(request):
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        form.instance.username = request.POST['email']
        if form.is_valid():
            login(request, form.save())
            UserInformation.objects.create(user=request.user)
            return redirect('home')
    context = {'form': form}
    return render(request, 'seminar/signup.html', context)


# Signup options for organization
def organizationsignup(request):
    form_a = UserForm()
    form_b = OrganizationForm()
    if request.method == 'POST':
        form_a = UserForm(request.POST)
        form_b = OrganizationForm(request.POST)
        form_a.instance.username = request.POST['email']
        if form_a.is_valid() and form_a.is_valid():
            login(request, form_a.save())
            form_b.instance.user = request.user
            form_b.save()
            return redirect('home')
    context = {
        'form_a': form_a,
        'form_b': form_b
    }
    return render(request, 'seminar/organizationsignup.html', context)


# Login to system
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


# Logout
def signout(request):
    logout(request)
    return redirect('signin')


def main(request):
    user = request.user
    seminars = Seminar.objects.all()
    org_access = is_organization(user)
    user_access = is_user(user)
    context = {
        'seminars': seminars,
        'org_access': org_access,
        'user_access': user_access,
    }
    return render(request, 'seminar/main.html', context)

# Home View


def home(request):
    user = request.user
    seminars = Seminar.objects.all()
    latest_seminars = seminars.order_by('-id')[:3]
    print("rev--------------------------------")
    print(latest_seminars)
    print("not--------------------------------")
    print(seminars)
    org_access = is_organization(user)
    user_access = is_user(user)
    

    context = {
        'seminars': seminars,
        'latest_seminars':latest_seminars,
    }
    return render(request, 'seminar/home.html', context)

# View all events
def seminars(request):
    user = request.user
    seminarss = Seminar.objects.all()
    seminars = seminarss.order_by('-id')[::1]
    print("rev--------------------------------")
    print(seminars)
    print("not--------------------------------")
    print(seminarss)
    org_access = is_organization(user)
    user_access = is_user(user)
    

    context = {
        'seminars': seminars,
    }
    return render(request, 'seminar/seminars.html', context)




# To show seminar's detailed information and Also allow users to register




def seminardetails(request, pk_test):
    seminar = Seminar.objects.get(id=pk_test)
    user = UserInformation.objects.filter(user=request.user.id).first()
    registered_seminar = False
    if user is not None:
        registered_seminar = Registration.objects.filter(
            user=user.id, seminar=seminar.id).first()

    if request.method == 'POST':

        register = Registration(user=user, seminar=seminar)
        seminar.seat = seminar.seat-1

        # send email
        subject = 'Hello ' + user.user.email
        message = 'Successfully registered to the even'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [user.user.email]
        send_mail(subject, message, from_email, recipient_list)

        register.save()
        seminar.save()

        return HttpResponseRedirect(request.path_info)

    context = {
        'seminar': seminar,
        'registered_seminar': registered_seminar,
    }

    return render(request, 'seminar/seminardetails.html', context)

# Cancel Registration
def cancelRegistration(request, pk_test):
    seminar = Seminar.objects.get(id=pk_test)
    user = UserInformation.objects.filter(user=request.user.id).first()
    registered_seminar=False
    
    if request.method == 'POST':
        delete_regestration = get_object_or_404(Registration,seminar=seminar.id,user=user.id)
        delete_regestration.delete()
        seminar.seat += 1
        seminar.save()
        return redirect('seminars')

    context = {
        'seminar': seminar,
        'registered_seminar': registered_seminar,
    }

    return render(request, 'seminar/seminardetails.html', context)

# seminar archive . Report on the seminar


def seminararchive(request, pk_test):
    seminar = Seminar.objects.get(id=pk_test)

    context = {
        'seminar': seminar,
    }
    return render(request, 'seminar/seminararchive.html', context)

# Events where User registered


@login_required(login_url='signin')
@user_access_only()
def myseminar(request):
    user = UserInformation.objects.get(user=request.user.id)

    seminars = Registration.objects.filter(user= user.id)
    #seminars = Registration.objects.all()
    #for i in seminars:
       # print("\\\\\\\\\\\\\\\\\\\\\\\\\\\\")
        #print(i)
    context = {
        'seminars': seminars,
    }
    return render(request, 'seminar/myseminar.html', context)


# To add seminar to the system and only organization can access this section
@login_required(login_url='signin')
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


# Events organized by individual organization
@login_required(login_url='signin')
@organization_access_only()
def organizedseminar(request):
    organization = Organization.objects.get(user=request.user.id)
    seminars = Seminar.objects.filter(organization=organization.id)

    context = {
        'seminars': seminars
    }
    return render(request, 'seminar/organizedseminar.html', context)


# Organization see a particular organized event's detailed information and list of users registered to the events
@login_required(login_url='signin')
@organization_access_only()
def organizedseminardetails(request, pk_test):
    org = Organization.objects.get(user=request.user.id)
    seminar = get_object_or_404(Seminar,id=pk_test,organization=org)
    r_users = Registration.objects.filter(
        seminar=seminar.id)
    if request.method == 'POST':
        user_id = request.POST['id_submit']
        delete_regestration = Registration.objects.get(id=user_id)
    
        delete_regestration.delete()
        seminar.seat += 1
        seminar.save()
        return HttpResponseRedirect(request.path_info)
    context = {
        'seminar': seminar,
        'r_users': r_users,
    }

    return render(request, 'seminar/organizedseminardetails.html', context)


@login_required(login_url='signin')
@user_access_only()
def user_info(request):
    print('user Info: ---------------------------------------- ')
    print( request.user.id)
    
    user_acc =get_object_or_404(UserInformation,user=request.user.id)
    #print('user Info:  '+ user_acc)
    context={
        'user_acc':user_acc,
    }
    return render(request, 'seminar/user_info.html', context )



@login_required(login_url='signin')
@user_access_only()
def user_info_update(request):

    user_acc = UserInformation.objects.get(user=request.user.id)
    form = UserInformationForm(request.POST or None, request.FILES or None, instance=user_acc)
    if form.is_valid():
        form.save()
        return redirect('user_info')


    context={
        'user_acc':user_acc,
        'form':form,
    }
    return render(request, 'seminar/user_info_update.html', context )

@login_required(login_url='signin')
@organization_access_only()
def organization_info(request):
    user_acc = Organization.objects.get(user=request.user.id)
    context={
        'user_acc':user_acc,
    }
    return render(request, 'seminar/organization_info.html', context )

@login_required(login_url='signin')
@organization_access_only()
def organization_info_update(request):
    user_acc = Organization.objects.get(user=request.user.id)
    form = OrganizationForm(request.POST or None, request.FILES or None, instance=user_acc)
    if form.is_valid():
        form.save()
        return redirect('organization_info')


    context={
        'user_acc':user_acc,
        'form':form,
    }
    return render(request, 'seminar/organization_info_update.html', context )


def about_us(request):
    return render(request,'seminar/about.html')    


@login_required(login_url='signin')
@organization_access_only()
def update_seminar_details(request,pk_test):
    org = Organization.objects.get(user=request.user.id)
    seminar = get_object_or_404(Seminar,id=pk_test,organization=org)
    form = SeminarForm(request.POST or None, request.FILES or None, instance=seminar)
    if form.is_valid():
        form.save()
        return redirect('organizedseminar')


    context={
        'seminar':seminar,
        'form':form,
    }
    return render(request, 'seminar/update_seminar_details.html', context )
