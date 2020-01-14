from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

# Custom imports
from submissions.models import Submission
from submissions.forms import SubmissionForm, EditSubmissionForm
from users.models import Student
from events.models import Event



def submission_detail(request, pk, template_name="submissions/submission_detail.html"):

    try:
        submission = Submission.objects.get(pk=pk)
    except Submission.DoesNotExist:
        raise Http404("This submission does not exist :0")

    submission.status_background = get_status_background(submission.status)
    submission.progress_background = get_progress_background(submission.progress_percentage)

    context = {
        'submission': submission,
        "students": submission.students.all(),
    }

    return render(request, template_name, context)



def submission_list(request, template_name="submissions/submission_list.html"):
    
    submissions = Submission.objects.all()
    n_submitted, approval_rate = get_statistics()

    for sub in submissions:
        sub.status_background = get_status_background(sub.status)

    context = {
        'submissions': submissions,
        'total_submissions':n_submitted,
        'approval_rate': approval_rate,
    }

    return render(request, template_name, context)


@login_required
def submission_create(request, event_pk, template_name="submissions/submission_form.html"):
    
    form = SubmissionForm(request.POST or None)
    event = Event.objects.get(id=event_pk)

    if request.POST:
        if form.is_valid():
            submission = form.save(commit=False)
            submission.user = request.user
            submission.event = event
            submission.save()
            form.save_m2m()
            new_submission_message = "Created submission successfully"
            messages.success(request, new_submission_message)
            return redirect("submissions:submission_list")
        else:
            for msg in form._errors:
                messages.error(request, f"{form._errors[msg]}")

    return render(request, template_name, {"form": form, "event":event})


@login_required
def submission_update(request, pk, template_name="submissions/submission_form.html"):
    if request.user.is_superuser:
        submission = get_object_or_404(Submission, pk=pk)
    else:
        submission = get_object_or_404(Submission, pk=pk)

    form = EditSubmissionForm(request.POST or None, instance=submission)

    if request.POST:
        if form.is_valid():
            form.save()
            return redirect(f"/submissions/{pk}")
        else:
            for msg in form._errors:
                messages.error(request, f"{form._errors[msg]}")

    return render(request, template_name, {"form": form})


@login_required
def submission_delete(request, pk, template_name="submissions/submission_confirm_delete.html"):
    submission = get_object_or_404(Submission, pk=pk)
    
    if request.method == "POST":
        submission.delete()
        delete_message = "Successfully deleted that submission ;)"
        messages.success(request, delete_message)

        return redirect("submissions:submission_list")

    return render(request, template_name, {"submission": submission})


@login_required
def submission_done(request, pk):
    if request.user.is_superuser:
        submission = get_object_or_404(Submission, pk=pk)
    else:
        event = get_object_or_404(Submission, pk=pk, students=request.user)
    submission.submitted = True
    submission.save()
    return redirect(f"/submissions/{pk}")

@login_required
def submission_undone(request, pk):
    if request.user.is_superuser:
        submission = get_object_or_404(Submission, pk=pk)
    else:
        submission = get_object_or_404(Submission, pk=pk, students=request.user)
    submission.submitted = False
    submission.save()
    return redirect(f"/submissions/{pk}")



def get_statistics():
    ''' This method get some statistics on the Submission instances '''
    # Only submission with status__in the values below are accounted for statistics
    n_submitted = Submission.objects.filter(status__in=[2,3,4]).count()
    n_approved = Submission.objects.filter(status=3).count()
    approval_rate = 0
    if n_submitted > 0:
        approval_rate =  n_approved // n_submitted *100
    return n_submitted, approval_rate


def get_status_background(status):
    """
    Gets the appropriate button color for a given status of a submission
    :param progress: The current status of a submission instance, check Submission model for choices field
    :return: a string representing the corresponding button
    """
    color = ""
    status = int(status)
    if status == 0 or status == 1:
        color = "light"
    elif status == 2:
        color = "warning"
    elif status == 3:
        color = "success"
    elif status ==4:
        color = "danger"
    else:
        color = "light"

    return color

def get_progress_background(progress):
    """
    Gets the appropriate background color for a given amount of progress made in a submisison
    :param progress: the amount of progress between the start date and the ending date (0-100)
    :return: a string representing the corresponding color for a background with the given amount of progress
    """
    if progress == 100:
        color = "success"
    elif progress >= 65 and progress < 100:
        color = "warning"
    elif progress < 65:
        color = "danger"
    else:
        color = "danger"

    return color