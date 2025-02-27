from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm 
from django.contrib import messages
from users import forms 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User

# Create your views here.
def sign_up(request):
    if request.method == "POST":
        form = forms.CustomRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Account created successfully')  
            user = form.save(commit=False)
            user.set_password(request.POST.get("password1"))
            user.is_active=False
            user.save()
            messages.success(request, 'A Confirmation mail sent. Please check your email')
            return redirect("sign-in")


    else:
        form = forms.CustomRegistrationForm()


    return render(request, "registration/register.html", {"form": form})

def sign_in(request):
    form = forms.LoginForm()
    if request.method == "POST":
        form = forms.LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
    return render(request, "registration/login.html", {"form": form})

def sign_out(request):
    if request.method == "POST":
        logout(request)
        return redirect("sign-in")
    
def activate_user(request, user_id, token):
    try:
        user = User.objects.get(id=user_id)
        if default_token_generator.check_token(user, token):
            user.is_active = True 
            user.save()
            messages.success(request, "account activated successfully")
            return redirect("sign-in")
        else:
            return HttpResponse('Invalid Id or token')
    except User.DoesNotExist:
        return HttpResponse('User does not exist')