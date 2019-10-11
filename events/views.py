from django.http import Http404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

# custom imports
from events.models import Event
from users.models import Student
from events.forms import EventForm
from datetime import datetime


def event_detail(request, pk, template_name="events/event_detail.html"):

    try:
        event = Event.objects.get(pk=pk)
    except Event.DoesNotExist:
        raise Http404("This Event does not exist :0")

    event = get_context(event)

    context = {"event": event, "students": event.students.all()}
    return render(request, template_name, context)


# @login_required (use this decorator if deadlines must be seen only by users)
def event_list(request, template_name="events/event_list.html"):
    events = Event.objects.all()
    context = {}

    events = [get_context(t) for t in events]

    context["current_events"], context["past_events"] = filter_events(events)

    return render(request, template_name, context)


@login_required
def event_create(request, template_name="events/event_form.html"):
    form = EventForm(request.POST or None)

    if form.is_valid():
        event = form.save(commit=False)
        event.user = request.user
        event.save()
        form.save_m2m()
        return redirect("events:event_list")

    return render(request, template_name, {"form": form})


@login_required
def event_update(request, pk, template_name="events/event_form.html"):
    if request.user.is_superuser:
        event = get_object_or_404(Event, pk=pk)
    else:
        event = get_object_or_404(Event, pk=pk)
    form = EventForm(request.POST or None, instance=event)

    if form.is_valid():
        form.save()
        return redirect(f"/events/{pk}")

    return render(request, template_name, {"form": form})


@login_required
def event_delete(request, pk, template_name="events/event_confirm_delete.html"):
    if request.user.is_superuser:
        event = get_object_or_404(Event, pk=pk)
    else:
        event = get_object_or_404(Event, pk=pk, students=request.user)
    if request.method == "POST":
        event.delete()
        return redirect("events:event_list")
    return render(request, template_name, {"object": event})


@login_required
def event_done(request, pk):
    if request.user.is_superuser:
        event = get_object_or_404(Event, pk=pk)
    else:
        event = get_object_or_404(Event, pk=pk, students=request.user)
    event.is_done =  True
    event.save()
    return redirect(f"/events/{pk}")

@login_required
def event_undone(request, pk):
    if request.user.is_superuser:
        event = get_object_or_404(Event, pk=pk)
    else:
        event = get_object_or_404(Event, pk=pk, students=request.user)
    event.is_done =  False
    event.save()
    return redirect(f"/events/{pk}")


# Auxiliar methods:


def filter_events(events):
    """ 
    This method filter Event instances in two categories
    current events and past event, depending on the days_left field
     """
    current_events = list(filter(lambda t: (t.days_left >= 0 and not t.is_done), events))
    past_events = list(filter(lambda t: (t.days_left < 0 or t.is_done), events))

    return current_events, past_events

def get_context(event):
    '''
    Some context is required for each Event
    '''
    event.days_left = get_days_left(event.deadline)
    event.progress_percentage = get_progress_percentage(event)
    event.progress_background = get_progress_background(event.progress_percentage)
    return event

def get_days_left(deadline):
    """ Used to calculate how many days are left until a event deadline """
    now = datetime.now().date()
    days_left = (deadline - now).days
    return days_left


def get_progress_percentage(event):
    """ Return the percentage of time left for a certain event based on its deadline date """
    created_at_date = event.created_at.date()
    total_days = (event.deadline - created_at_date).days
    if event.is_done:
        return 100
    progress_percentage = (
        100 - (100 * event.days_left / total_days) if event.days_left > 0 else 100
    )
    return int(progress_percentage)


def get_progress_background(progress):
    """
    Gets the appropriate background color for a given amount of progress made in a project
    :param progress: the amount of progress between the start date and the ending date (0-100)
    :return: a string representing the corresponding color for a background with the given amount of progress towards
    the end date
    """
    if progress == 100:
        background_color = "info"
    elif progress >= 90:
        background_color = "danger"
    elif progress >= 70:
        background_color = "warning"
    else:
        background_color = "success"

    return background_color
