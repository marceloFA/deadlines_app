from django import forms
from django.http import Http404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

# custom imports
from tasks.models import Task, SubTask
from users.models import Student
from tasks.forms import TaskForm, SubTaskForm
from datetime import datetime


def task_detail(request, pk, template_name="tasks/task_detail.html"):

    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        raise Http404("This Task does not exist :0")

    if request.method == 'POST': 
        toggle(task,request.POST)
        if request.POST.get('add_subtask'): 
            ''' A Subtask object is created and saved '''
            subtask = SubTask(name = request.POST.get('add_subtask') , task = task) 
            subtask.save()

    subtask_form = SubTaskForm(task = task)
    task.days_left = get_days_left(task.deadline)
    task.progress_percentage = task.get_progress_percentage
    task.progress_background = task.progress_color

    context = {}
    context['task'] = task
    context['students'] = task.students.all()
    context['subtasks'] = subtask_form
    
    return render(request, template_name, context)


# @login_required (use this decorator if deadlines must be seen only by users)
def task_list(request, template_name="tasks/task_list.html"):
    tasks = Task.objects.all()
    context = {}

    for t in tasks:
        t.days_left = get_days_left(t.deadline)

    context["current_tasks"], context["past_tasks"] = filter_tasks(tasks)

    return render(request, template_name, context)


@login_required
def task_create(request, template_name="tasks/task_form.html"):
    form = TaskForm(request.POST or None)

    if form.is_valid():
        task = form.save(commit=False)
        task.user = request.user
        task.save()
        form.save_m2m()
        return redirect("tasks:task_list")

    return render(request, template_name, {"form": form})


@login_required
def task_update(request, pk, template_name="tasks/task_form.html"):
    if request.user.is_superuser:
        task = get_object_or_404(Task, pk=pk)
    else:
        task = get_object_or_404(Task, pk=pk)
    form = TaskForm(request.POST or None, instance=task)

    if form.is_valid():
        form.save()
        return redirect(f"/tasks/{pk}")

    return render(request, template_name, {"form": form})


@login_required
def task_delete(request, pk, template_name="tasks/task_confirm_delete.html"):
    if request.user.is_superuser:
        task = get_object_or_404(Task, pk=pk)
    else:
        task = get_object_or_404(Task, pk=pk, students=request.user)
    if request.method == "POST":
        task.delete()
        return redirect("tasks:task_list")
    return render(request, template_name, {"object": task})


@login_required
def task_done(request, pk):
    if request.user.is_superuser:
        task = get_object_or_404(Task, pk=pk)
    else:
        task = get_object_or_404(Task, pk=pk, students=request.user)
    task.is_done =  True
    task.save()
    return redirect(f"/tasks/{pk}")

@login_required
def task_undone(request, pk):
    if request.user.is_superuser:
        task = get_object_or_404(Task, pk=pk)
    else:
        task = get_object_or_404(Task, pk=pk, students=request.user)
    task.is_done =  False
    task.save()
    return redirect(f"/tasks/{pk}")

def get_progress_percentage_subtasks(task):
    """ Returns the percentage based on the subtasks completed, and also based on the deadline """
    subtasks = SubTask.objects.all().filter(task = task)
    total_subtasks , completed_subtasks = len(subtasks) , 0
    for subtask in subtasks:
        if subtask.is_done:
            completed_subtasks+=1
    
    if (task.deadline - datetime.now().date()).days <= 0 or task.is_done:
        progress_percentage = 100
    elif total_subtasks == 0:
        progress_percentage = 0
    else:
        progress_percentage = int((completed_subtasks/total_subtasks)*100)
    return progress_percentage


def filter_tasks(tasks):
    """ This method filter Task instances in two categoires
         current tasks and past task, depending on the days_left field
     """
    current_tasks = list(filter(lambda t: (t.days_left >= 0 and not t.is_done), tasks))
    past_tasks = list(filter(lambda t: (t.days_left < 0 or t.is_done), tasks))

    return current_tasks, past_tasks

def toggle(task, data):
    ''' Toggles completion of subtasks based on form data '''
    subtasks = SubTask.objects.all().filter(task = task)
    for subtask in subtasks:
        if data.get(subtask.name):
            subtask.is_done = True
        else:
            subtask.is_done = False
        subtask.save()
