from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages,auth

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]

            user = Account.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=username,
                password=password
            )
            user.phone_number = phone_number
            user.save()
            messages.success(request,'Registration Successful. ')


            # Redirect to login page after successful registration
            return redirect('register')  # Replace 'login' with your URL name
    else:
        form = RegistrationForm()  # For GET requests

    # Always define context and return HttpResponse
    context = {'form': form}
    return render(request, 'accounts/register.html', context)


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email,password=password)

        if user is not None:
            auth.login(request,user)
            #messages.success(request,'You are now logged in. ')
            return redirect('home')
        else:
            messages.error(request,'Invalid Login')
            return redirect('login')
    return render(request,'accounts/login.html')


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request,'You are logged out. ')
    return redirect('login')