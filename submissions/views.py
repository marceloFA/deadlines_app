from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q

# Custom imports
from tasks.models import Task
from submissions.models import Submission
from submissions.forms import SubmissionForm
from users.models import Student



def submission_detail(request, pk, template_name="submissions/submission_detail.html"):

    try:
        submission = Submission.objects.get(pk=pk)
    except Submission.DoesNotExist:
        raise Http404("This submission does not exist :0")

    submission.status_background = get_status_background(submission.status)

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
        'submissions':submissions,
        'total_submissions':n_submitted,
        'approval_rate': approval_rate,
    }

    return render(request, template_name, context)


def get_statistics():
    n_submitted = Submission.objects.filter(status__in=[3,4,5]).count()
    n_approved = Submission.objects.filter(status=4).count()
    approval_rate = 0
    if n_submitted > 0:
        approval_rate =  n_approved // n_submitted *100
    return n_submitted, approval_rate



@login_required
def submission_create(request, template_name="submissions/submission_form.html"):
    form = SubmissionForm(request.POST or None)

    if form.is_valid():
        submission = form.save(commit=False)
        submission.user = request.user
        submission.save()
        form.save_m2m()

        return redirect("submissions:submission_list")

    return render(request, template_name, {"form": form})


@login_required
def submission_update(request, pk, template_name="submissions/submission_form.html"):
    if request.user.is_superuser:
        submission = get_object_or_404(Submission, pk=pk)
    else:
        submission = get_object_or_404(Submission, pk=pk)

    form = SubmissionForm(request.POST or None, instance=submission)

    if form.is_valid():
        form.save()
        return redirect(f"/submissions/{pk}")

    return render(request, template_name, {"form": form})

@login_required
def submission_delete(request, pk, template_name="submissions/submission_confirm_delete.html"):
    if request.user.is_superuser:
        submission = get_object_or_404(Submission, pk=pk)
    else:
        submission = get_object_or_404(Submission, pk=pk, students=request.user)
    
    if request.method == "POST":
        submission.delete()
        return redirect("submissions:submission_list")

    return render(request, template_name, {"submission": submission})


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
    elif status == 2 or status == 3:
        color = "warning"
    elif status == 4:
        color = "success"
    elif status ==5:
        color = "danger"
    else:
        color = "light"

    return color
