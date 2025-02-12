from django.shortcuts import render
from tasks.forms import TaskForm, TaskModelForm
from django.http import HttpResponse
from tasks.models import Employee, Tasks, TaskDetails, Project
from django.db.models import Q, Prefetch, Count
import datetime


# Create your views here.
def dashboard(request):
    return render(request, "dashboard/manager-dashboard.html")


def user_dashboard(request):
    return render(request, "dashboard/user-dashboard.html")


def test(request):
    context = {"names": ["Nayeem", "Galib", "Sakib", "Affan"]}
    return render(request, "test.html", context)


def create_task(request):
    employees = Employee.objects.all()
    form = TaskModelForm()

    if request.method == "POST":
        form = TaskModelForm(request.POST)
        # print(form)
        if form.is_valid():
            """for django ModelForm data"""
            form.save()
            return render(
                request,
                "task_form.html",
                {"form": form, "message": "Task Created Successfully"},
            )

            """for django form data"""
            # data = form.cleaned_data
            # title = data.get("title")
            # description = data.get("description")
            # due_date = data.get("due_date")
            # assigned_to = data.get("assigned_to")
            # task = Tasks.objects.create(title=title, description=description, due_date=due_date)

            # for emp_id in assigned_to:
            #     employee = Employee.objects.get(id=emp_id)
            #     task.employees.add(employee)

            # return HttpResponse("Task Created Successfully")

    context = {"form": form}
    return render(request, "task_form.html", context)


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
    # tasks = TaskDetails.objects.exclude(priority="L")

    # show the task that contain the word 'th' and status is pending
    # tasks = Tasks.objects.filter(title__icontains = "Th", status="PENDING")
    
    # show the task that contain the word 'th' or status is pending
    # tasks = Tasks.objects.filter(Q(title__icontains = "Th") | Q(status="PENDING"))

    # # optimized
    # tasks = Tasks.objects.select_related("taskdetails").all()

    """ prefetch related (reverse Foriegn Key, manytomany) """
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
