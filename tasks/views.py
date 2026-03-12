from django.shortcuts import render, redirect, get_object_or_404
from .models import Task

def index(request):
    """
    Display all tasks and handle creation of new tasks.
    """
    tasks = Task.objects.all().order_by('-id')  # show latest tasks first

    if request.method == "POST":
        title = request.POST.get("title", "").strip()  # strip whitespace
        if title:  # prevent empty tasks
            Task.objects.create(title=title)
        return redirect('index')  # use named URL

    return render(request, "tasks/index.html", {"tasks": tasks})


def delete_task(request, task_id):
    """
    Delete a task by its ID.
    """
    task = get_object_or_404(Task, id=task_id)  # safer than Task.objects.get
    task.delete()
    return redirect('index')  # use named URL