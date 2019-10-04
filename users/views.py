from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from users.forms import StudentCreationForm, StudentChangeForm
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from .models import Student
from tasks.models import Task

def register(request):
    ''' Register a new Student '''
    form = StudentCreationForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            student = form.save(commit=False)
            student.save()
            new_account_message = 'Created account successfully'
            messages.success(request, new_account_message)
            login(request, student)
            logged_in_message = f'Now you\'re logged in as {student.name}' 
            messages.info(request, logged_in_message)
            return redirect('tasks:task_list')
        else:
            for msg in form.error_messages:
                messages.error(request, f"{form.error_messages[msg]}")
    
    # else it's a GET request:       
    context = {}
    context['form'] = form
    return render(request, 'register.html', context)


def login_request(request):

    ''' To log in a Student'''
    login_error_message = 'Invalid username or password :('

    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f'Now you\'re logged in as {username}')
                return redirect('tasks:task_list')
            else:
                messages.error(request, login_error_message)
        else:
            # prompt deactivated student to re-activate his account
            try:
                username = request.POST.get('username')
                user = Student.objects.get(username=username)
                messages.error(request, 'Your account has been deactivated so you must re-activate it before login.')
            # student is doesn't exists so we believe this is invalid login
            except Student.DoesNotExist:
                messages.error(request, login_error_message)

    
    # else it's a GET request:
    form = AuthenticationForm(request.POST or None)
    context = {}
    context['form'] = form
    return render(request, 'login.html', context)
    

def logout_request(request):
    ''' To log out a student '''
    logout(request)
    logged_out_message = "You logged out successfully"
    messages.success(request, logged_out_message)
    return redirect('tasks:task_list')

@login_required
def deactivate(request):
    ''' To deactivate Student '''
    if request.method == 'POST':
        password = request.POST.get('password')
        if request.user.check_password(password):
            request.user.is_active = False
            request.user.save()
            # NOTE: user will automatically log out
            messages.success(request, 'Your account has been deactivated')
            return redirect('tasks:task_list')
        else:
            messages.error(request, 'Invalid password')

    # else it's a GET request:
    return render(request, 'deactivation.html')

def reactivate(request):
    ''' To Reactivate Student '''
    login_error_message = 'Invalid username or password :('

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = Student.objects.get(username=username)
        if check_password(password, user.password):
            user.is_active = True
            user.save()
            login(request, user)
            messages.info(request, f'Reactivation is successful and now you\'re logged in as {username}')
            return redirect('tasks:task_list')
        else:
            messages.error(request, login_error_message)

    # else it's a GET request:
    return render(request, 'reactivation.html')

def show_profile(request):
    context = {}
    # Load related Tasks
    context['tasks'] = Task.objects.filter(students=request.user.id)
    return render(request, 'profile.html', context)
    
def student_update(request, pk):
    
    # Get student
    if request.user.is_superuser:
        student = get_object_or_404(Student, pk=pk)
    else:
        student = get_object_or_404(Student, pk=pk)
    
    # fill form 
    form = StudentChangeForm(request.POST or None, instance=student)
    context = {}
    context['form'] = form

    if request.method == 'POST':
        if form.is_valid():
            if(form.cleaned_data['username']):
                student.username = form.cleaned_data['username']
            if(form.cleaned_data['name']):
                student.name = form.cleaned_data['name']
            student.save()
            
            return redirect('tasks:task_list')
        else:
            for msg in form.error_messages:
                messages.error(request, f"{form.error_messages[msg]}")
    
    return render(request, 'edit-profile.html', context)