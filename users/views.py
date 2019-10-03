from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from users.forms import StudentCreationForm
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required

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
        print(password)
        if request.user.check_password(password):
            request.user.is_active = 0
            request.user.save()
            messages.success(request, 'Your account has been deactivated')
            return redirect('tasks:task_list')
        else:
            messages.error(request, 'Invalid password')

    # else it's a GET request:
    return render(request, 'deactivation.html')
