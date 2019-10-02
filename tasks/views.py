from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
# custom imports
from tasks.models import Task
from users.models import Student
from tasks.forms import TaskForm
from datetime import datetime


def task_detail(request, pk, template_name='tasks/task_detail.html'):
    
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        raise Http404('This Task does not exist :0')
    
    task.days_left = get_days_left(task.deadline)
    task.progress_percentage = get_progress_percentage(task)
    
    context = {}
    context['task'] = task
    context['students'] = task.students.all()
    return render(request, template_name, context)


#@login_required (use this decorator if deadlines must be seen only by users)
def task_list(request, template_name='tasks/task_list.html'):
    '''
    use this logic if deadlines must be seen only by users:
    if request.user.is_superuser:
        task = task.objects.all()
    else:
       task = task.objects.filter(user=request.user)
    '''
    tasks = Task.objects.all()
    context = {}

    for t in tasks:
        t.days_left = get_days_left(t.deadline)
    
    context['tasks'] = tasks

    return render(request, template_name, context)

@login_required
def task_create(request, template_name='tasks/task_form.html'):
    form = TaskForm(request.POST or None)
    
    if form.is_valid():
        task = form.save(commit=False)
        task.user = request.user
        task.save()
        form.save_m2m()
        return redirect('tasks:task_list')

    return render(request, template_name, {'form':form})


@login_required
def task_update(request, pk, template_name='tasks/task_form.html'):
    if request.user.is_superuser:
        task = get_object_or_404(Task, pk=pk)
    else:
        task = get_object_or_404(Task, pk=pk)

    form = TaskForm(request.POST or None, instance=task)

    if form.is_valid():
        form.save()

        return redirect('tasks:task_list')
    return render(request, template_name, {'form':form})

@login_required
def task_delete(request, pk, template_name='tasks/task_confirm_delete.html'):
    if request.user.is_superuser:
        task = get_object_or_404(Task, pk=pk)
    else:
        task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method=='POST':
        task.delete()
        return redirect('tasks:task_list')
    return render(request, template_name, {'object':task})



# Auxiliar methods:
def get_days_left(deadline):
    ''' Used to calculate how many days are left until a task deadline '''
    now = datetime.now().date()
    days_left = (deadline-now).days
    return days_left


def get_progress_percentage(task):
    ''' Return the percentage of time left for a certain task based on its deadline date '''
    created_at_date = task.created_at.date()
    total_days = (task.deadline - created_at_date).days 
    progress_percentage = 100 - (100 * task.days_left / total_days)
    return int(progress_percentage)