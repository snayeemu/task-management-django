from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm 
from django.contrib import messages
from users import forms 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Prefetch

def is_admin(user):
    return user.groups.filter(name="Admin").exists()

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

@login_required
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

@user_passes_test(is_admin, login_url="no-permission")
def admin_dashboard(request):
    users = User.objects.prefetch_related(
        Prefetch("groups", queryset=Group.objects.all(), to_attr="all_groups")
    ).all()
    for user in users:
        if user.all_groups:
            user.group_name = user.all_groups[0].name 
        else:
            user.group_name = "Group is not Assigned"


    return render(request, "admin/dashboard.html", {"users": users})

@user_passes_test(is_admin, login_url="no-permission")
def assign_role(request, user_id):
    user = User.objects.get(id = user_id)
    form = forms.AssignRoleForm()

    if request.method == "POST":
        form = forms.AssignRoleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data.get("role")
            user.groups.clear() # remove old roles
            user.groups.add(role)
            messages.success(request, f"User {user.username} has been assigned to the role {role.name}")
            return redirect("admin-dashboard")
    return render(request, "admin/assign-role.html", {"form": form})

@user_passes_test(is_admin, login_url="no-permission")
def create_group(request):
    form = forms.CreateGroupForm()

    if request.method == "POST":
        form = forms.CreateGroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            messages.success(request, f"Group {group.name} has been created successfully")
    return render(request, "admin/create-group.html", {"form": form})

@user_passes_test(is_admin, login_url="no-permission")
def group_list(request):
    groups = Group.objects.prefetch_related("permissions").all()
    return render(request, "admin/group-list.html", {"groups": groups})