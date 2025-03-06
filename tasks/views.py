from django.shortcuts import render, redirect
from tasks.forms import TasksForm, TasksModelForm, TasksDetailsModelForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse
from tasks.models import Tasks, TaskDetails, Project
from django.db.models import Q, Prefetch, Count
import datetime
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required


def is_manager(user):
    return user.groups.filter(name="Manager").exists()

def is_employee(user):
    return user.groups.filter(name="Employee").exists()

# Create your views here.
@user_passes_test(is_manager, login_url="no-permission")
def manager_dashboard(request):
    query = request.GET.get("type", "all")
    base_query = Tasks.objects.select_related("details").prefetch_related(
        "assigned_to"
    )
    tasks = None
    if query == "all":
        tasks = base_query.all()
    elif query == "completed":
        tasks = base_query.filter(status="COMPLETED")
    elif query == "in_progress":
        tasks = base_query.filter(status="IN_PROGRESS")
    elif query == "pending":
        tasks = base_query.filter(status="PENDING")

    counts = Tasks.objects.aggregate(
        total=Count("id"),
        completed=Count("id", Q(status="COMPLETED")),
        pending=Count("id", Q(status="PENDING")),
        in_progress=Count("id", Q(status="IN_PROGRESS")),
    )
    context = {"tasks": tasks, "counts": counts}
    return render(request, "dashboard/manager-dashboard.html", context)

@user_passes_test(is_employee, login_url="no-permission")
def employee_dashboard(request):
    return render(request, "dashboard/user-dashboard.html")

@login_required
@permission_required("tasks.add_tasks", login_url="no-permission")
def create_task(request):
    employees = User.objects.all() 
    task_form = TasksModelForm() 
    task_details_form = TasksDetailsModelForm() 

    if request.method == "POST":
        task_form = TasksModelForm(request.POST)
        task_details_form = TasksDetailsModelForm(request.POST)
        # print(form)
        if task_form.is_valid() and task_details_form.is_valid():
            """for django ModelForm data"""     
            task = task_form.save()
            task_details = task_details_form.save(commit=False)
            task_details.task = task
            task_details.save()
            messages.success(request, "Tasks Created Successfully")
            return redirect("create-task")

    context = {"task_form": task_form, "task_details_form": task_details_form}
    return render(request, "task_form.html", context)

@login_required
@permission_required("tasks.change_tasks", login_url="no-permission")
def update_task(request, id):
    task = Tasks.objects.get(id=id)
    task_form = TasksModelForm(instance=task)
    task_details_form = TasksDetailsModelForm(instance=task.details)

    if request.method == "POST":
        task_form = TasksModelForm(request.POST, instance=task)
        task_details_form = TasksDetailsModelForm(
            request.POST, instance=task.details
        )
        # print(form)
        if task_form.is_valid() and task_details_form.is_valid():
            """for django ModelForm data"""
            task = task_form.save()
            task_details = task_details_form.save(commit=False)
            task_details.task = task
            task_details.save()
            messages.success(request, "Tasks Updated Successfully")
            return redirect("update-task", id)

    context = {"task_form": task_form, "task_details_form": task_details_form}
    return render(request, "task_form.html", context)

@login_required
@permission_required("tasks.delete_tasks", login_url="no-permission")
def delete_task(request, id): 
    if request.method == "POST": 
        task = Tasks.objects.get(id=id)
        task.delete()
        messages.success(request, "Tasks Deleted Successfully")
        return redirect("manager-dashboard")
    else:
        messages.error(request, "Something wrong")
        return redirect("manager-dashboard")

@login_required
@permission_required("tasks.view_tasks", login_url="no-permission")
def view_tasks(request):
    # # show pending tasks
    # tasks = Tasks.objects.filter(status="PENDING")

    # # retrieve all tasks from the database
    # tasks = Tasks.objects.all()

    # # retrieve a specific data
    # task_3 = Tasks.objects.get(id=1)

    # # first task
    # first_task = Tasks.objects.first()

    # # show tasks which due date is today
    # tasks = Tasks.objects.filter(due_date=datetime.date.today())

    # Exclude low priority tasks
    # tasks = TasksDetails.objects.exclude(priority="L")

    # show the task that contain the word 'th' and status is pending
    # tasks = Tasks.objects.filter(title__icontains = "Th", status="PENDING")

    # show the task that contain the word 'th' or status is pending
    # tasks = Tasks.objects.filter(Q(title__icontains = "Th") | Q(status="PENDING"))

    # # optimized
    # tasks = Tasks.objects.select_related("taskdetails").all()

    """prefetch related (reverse Foreign Key, manytomany)"""
    # # tasks = Project.objects.prefetch_related(Prefetch("tasks_set")).all()
    # tasks = Tasks.objects.prefetch_related("employees").all()

    # # aggregate function
    # task_count = Tasks.objects.aggregate(num_task = Count("id"))
    projects = Project.objects.annotate(num_tasks=Count("tasks")).order_by("-num_tasks")
    return render(
        request,
        "show_tasks.html",
        {"projects": projects},
    )

def task_details(request, id):
    task = Tasks.objects.get(id=id)
    return render(request, "task_details.html", {"task": task})