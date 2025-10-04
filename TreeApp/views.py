from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
import json
from django.views.decorators.http import require_POST
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden ,JsonResponse


# Create your views here.


def homepage(request):
    trees = TreeProfile.objects.all()
    # Convert QuerySet to list of dicts
    trees_data = list(trees.values('street_name', 'scientific_name', 'description', 'latitude', 'longitude'))
    # JSON encode it safely
    trees_json = json.dumps(trees_data, cls=DjangoJSONEncoder)
    return render(request, 'HomePage.html', {'trees_json': trees_json})

def TreeProfiles(request):

    TreeProfiles = TreeProfile.objects.all()
    
    context = {
            'TreeProfiles': TreeProfiles
        }
    print(TreeProfiles)  
    return render(request, 'Trees/TreeProfiles.html', context=context)

def add_tree(request):
    if request.method == 'POST':
        form = add_tree_ajax(request.POST)
        if form.is_valid():
            tree = form.save(commit=False)
            tree.submitted_by = request.user
            tree.save()
            return redirect('home')  # or wherever you want
    else:
        form = add_tree_ajax()
    return render(request, 'add_tree.html', {'form': form})


# Dashboard
@login_required
def dashboard(request):
    context = {}

    if request.user.user_type == "common":
        context["my_requests"] = TreeRequest.objects.filter(requester=request.user, status="pending")
        context["my_approved"] = TreeRequest.objects.filter(requester=request.user, status="answered")

    elif request.user.user_type == "contributor":
        context["all_requests"] = TreeRequest.objects.filter(status="pending")
        context["my_answers"] = TreeAnswer.objects.filter(contributor=request.user)

    return render(request, "Request/dashboard.html", context)
@login_required
@require_POST
def ajax_create_request(request):
    if request.user.user_type != "common":
        raise PermissionDenied

    form = TreeRequestForm(request.POST)
    if form.is_valid():
        tree_request = form.save(commit=False)
        tree_request.requester = request.user
        tree_request.save()
        return JsonResponse({
            "success": True,
            "id": tree_request.id,
            "title": tree_request.title,
            "description": tree_request.description,
            "location": tree_request.location,
            "status": tree_request.status
        })
    return JsonResponse({"success": False, "errors": form.errors})


@login_required
@require_POST
def ajax_update_request(request, request_id):
    tree_request = TreeRequest.objects.filter(id=request_id, requester=request.user).first()
    if not tree_request or request.user.user_type != "common":
        raise PermissionDenied

    if tree_request.status != "pending":
        return JsonResponse({"success": False, "error": "Cannot edit answered requests."})

    form = TreeRequestForm(request.POST, instance=tree_request)
    if form.is_valid():
        form.save()
        return JsonResponse({
            "success": True,
            "id": tree_request.id,
            "title": tree_request.title,
            "description": tree_request.description,
            "location": tree_request.location
        })
    return JsonResponse({"success": False, "errors": form.errors})


@login_required
@require_POST
def ajax_delete_request(request, request_id):
    tree_request = TreeRequest.objects.filter(id=request_id, requester=request.user).first()
    if not tree_request or request.user.user_type != "common":
        raise PermissionDenied

    tree_request.delete()
    return JsonResponse({"success": True, "id": request_id})

# Contributor: answer a request
@login_required
def answer_request(request, request_id):
    if request.user.user_type != "contributor":
        return HttpResponseForbidden("Only contributors can answer requests.")

    tree_request = get_object_or_404(TreeRequest, id=request_id)

    if request.method == "POST":
        form = TreeAnswerForm(request.POST, request.FILES)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.request = tree_request
            answer.contributor = request.user
            answer.save()

            # update request status
            tree_request.status = "answered"
            tree_request.save()

            return redirect("contributor_dashboard")

    else:
        form = TreeAnswerForm()

    return render(request, "requests/answer_request.html", {"form": form, "tree_request": tree_request})