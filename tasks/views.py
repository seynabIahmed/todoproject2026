from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import TaskForm
from .models import Task


@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user).order_by("completed", "due_date")
    return render(request, "tasks/task_list.html", {"tasks": tasks})


@login_required
def task_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect("tasks:list")
    else:
        form = TaskForm()

    return render(request, "tasks/task_form.html", {"form": form})
