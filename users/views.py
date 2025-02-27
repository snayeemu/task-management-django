from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm 
from django.contrib import messages
from users import forms 
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def sign_up(request):
    if request.method == "POST":
        form = forms.CustomRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Account created successfully')  
            user = form.save()
            user.set_password(request.POST.get("password1"))
            user.save()


    else:
        form = forms.CustomRegistrationForm()


    return render(request, "registration/register.html", {"form": form})

def sign_in(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        print("doc:", username, password)
        user = authenticate(username=username, password=password)
        print(user)
        if user:
            login(request, user)
            return redirect("home")
    return render(request, "registration/login.html")

def sign_out(request):
    if request.method == "POST":
        logout(request)
        return redirect("sign-in")