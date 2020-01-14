from django.http import Http404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

# custom imports
from events.models import Event
from users.models import Student
from submissions.models import Submission
from submissions.views import get_status_background
from events.forms import EventForm
from datetime import datetime


def event_detail(request, pk, template_name="events/event_detail.html"):

    try:
        event = Event.objects.get(pk=pk)
    except Event.DoesNotExist:
        raise Http404("This Event does not exist :0")
    
    
    submissions = Submission.objects.filter(event=event)
    event = get_context(event)

    for sub in submissions:
        sub.status_background = get_status_background(sub.status)
    
    context = {"event": event, "submissions": submissions}
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
        event = get_object_or_404(Event, pk=pk)
    if request.method == "POST":
        event.delete()
        return redirect("events:event_list")
    return render(request, template_name, {"object": event})


# Auxiliar methods:
def filter_events(events):
    """ 
    This method filter Event instances in two categories
    current events and past event, depending on the days_left field
     """
    current_events = list(filter(lambda t: (t.days_left >= 0), events))
    past_events = list(filter(lambda t: (t.days_left < 0), events))

    return current_events, past_events

def get_context(event):
    '''
    Some context is required for each Event
    '''
    event.days_left = get_days_left(event.deadline)
    return event

def get_days_left(deadline):
    """ Used to calculate how many days are left until a event deadline """
    now = datetime.now().date()
    days_left = (deadline - now).days
    return days_left