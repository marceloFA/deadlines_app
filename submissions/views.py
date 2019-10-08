from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

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

    context = {
        'submission': submission,
        "students": submission.students.all(),
    }

    return render(request, template_name, context)



def submission_list(request, template_name="submissions/submission_list.html"):
    
    submissions = Submission.objects.all()
    for sub in submissions:
        sub.staus_background = get_status_background(sub.status)

    context = {
        'submissions':submissions,
    }

    return render(request, template_name, context)


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
def submission_update(request, template_name="submissions/submission_form.html"):
    pass

@login_required
def submission_delete(request, template_name="submissions/submission_confirm_delete.html"):
    pass


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
