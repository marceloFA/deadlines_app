from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required

# Custom imports
from users.forms import StudentCreationForm, StudentChangeForm, AccountDeactivationForm, \
    ReactivationForm
from .models import Student
from events.models import Event
from events.views import get_events_context, filter_events
from submissions.models import Submission
from submissions.views import get_submissions_and_context



def register(request):
    """ Register a new Student """
    form = StudentCreationForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            student = form.save(commit=False)
            student.save()
            new_account_message = "Created account successfully"
            messages.success(request, new_account_message)
            login(request, student)
            logged_in_message = f"Now you're logged in as {student.name}"
            messages.info(request, logged_in_message)
            return redirect("events:event_list")
        else:
            for msg in form._errors:
                messages.error(request, f"{form._errors[msg]}")

    # else it's a GET request:
    context = {"form": form}
    return render(request, "register.html", context)


def login_request(request):

    """ To log in a Student"""
    login_error_message = "Invalid username or password :("

    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Now you're logged in as {username}")
                return redirect("events:event_list")
            else:
                messages.error(request, login_error_message)
        else:
            # prompt deactivated student to re-activate his account
            try:
                username = request.POST.get("username")
                user = Student.objects.get(username=username)
                messages.error(
                    request,
                    "Your account has been deactivated so you must re-activate it before login.",
                )
            # student is doesn't exists so we believe this is invalid login
            except Student.DoesNotExist:
                messages.error(request, login_error_message)

    # else it's a GET request:
    form = AuthenticationForm(request.POST or None)
    context = {"form": form}
    return render(request, "login.html", context)


def logout_request(request):
    """ To log out a student """
    logout(request)
    logged_out_message = "You logged out successfully"
    messages.success(request, logged_out_message)
    return redirect("events:event_list")


@login_required
def deactivate(request):
    """ To deactivate Student """

    if request.method == "POST":
        password = request.POST.get("password")

        if request.user.check_password(password):
            request.user.is_active = False
            request.user.save()
            # NOTE: user will automatically log out
            messages.success(request, "Your account has been deactivated")
            return redirect("events:event_list")
        else:
            messages.error(request, "Invalid password")

    # else it's a GET request:
    form = AccountDeactivationForm(request.POST or None)
    context = {"form": form}
    return render(request, "deactivation.html", context)


def reactivate(request):
    """ To Reactivate Student """
    login_error_message = "Invalid username or password :("

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = Student.objects.get(username=username)
        if check_password(password, user.password):
            user.is_active = True
            user.save()
            login(request, user)
            messages.info(
                request,
                f"Reactivation is successful and now you're logged in as {username}",
            )
            return redirect("events:event_list")
        else:
            messages.error(request, login_error_message)

    # else it's a GET request:
    form = ReactivationForm(request.POST or None)
    context = {"form": form}
    return render(request, "reactivation.html", context)


@login_required
def show_profile(request):
    # Load related Events and submissions
    
    current_submissions, past_submissions = get_submissions_and_context(request.user.id)
    
    events = [get_events_context(event) for event in Event.objects.all()]
    current_events, past_events = filter_events(events)

    context = {
        "current_submissions": current_submissions,
        "past_submissions": past_submissions,
        "current_events": current_events,
        "past_events": past_events,
        }

    return render(request, "profile.html", context)


@login_required
def student_update(request, pk):

    # Get student
    if request.user.is_superuser:
        student = get_object_or_404(Student, pk=pk)
    else:
        student = get_object_or_404(Student, pk=pk)

    # fill form
    form = StudentChangeForm(request.POST or None, instance=student)
    context = {"form": form}

    if request.method == "POST":
        if form.is_valid():
            if form.cleaned_data["username"]:
                student.username = form.cleaned_data["username"]
            if form.cleaned_data["name"]:
                student.name = form.cleaned_data["name"]
            student.save()

            return redirect("events:event_list")
        else:
            for msg in form.error_messages:
                messages.error(request, f"{form.error_messages[msg]}")

    return render(request, "edit-profile.html", context)
