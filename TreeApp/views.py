from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
import json
from django.views.decorators.http import require_POST
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden ,JsonResponse
from django.utils import timezone
from django.db.models import Count

# Create your views here.


def homepage(request):
    # Get all trees
    trees = TreeProfile.objects.all().values(
        'street_name', 'description', 'latitude', 'longitude'
    )
    # Convert queryset to JSON safely
    trees_json = json.dumps(list(trees), cls=DjangoJSONEncoder)
    return render(request, 'HomePage.html', {'trees_json': trees_json})



def TreeProfiles(request):

    TreeProfiles = TreeProfile.objects.all()
    
    context = {
            'TreeProfiles': TreeProfiles
        }
    print(TreeProfiles)  
    return render(request, 'Trees/TreeProfiles.html', context=context)

# def add_tree(request):
#     if request.method == 'POST':
#         form = add_tree_ajax(request.POST)
#         if form.is_valid():
#             tree = form.save(commit=False)
#             tree.submitted_by = request.user
#             tree.save()
#             return redirect('home')  # or wherever you want
#     else:
#         form = add_tree_ajax()
#     return render(request, 'add_tree.html', {'form': form})

def get_trees_json(request):
    trees = []
    for tree in TreeProfile.objects.all():
        first_photo = tree.photos.first()
        trees.append({
            "id": tree.id,
            "street_name": tree.street_name,
            "description": tree.description,
            "latitude": float(tree.latitude),
            "longitude": float(tree.longitude),
            "image_url": first_photo.image.url if first_photo else ""
        })
    return JsonResponse(trees, safe=False)

@login_required
@csrf_exempt
def add_tree_ajax(request):
    if request.method == 'POST':
        try:
            street_name = request.POST.get('street_name')
            scientific_name = request.POST.get('scientific_name')
            habitat = request.POST.get('habitat')
            description = request.POST.get('description')
            rarity_status = request.POST.get('rarity_status')
            height_m = request.POST.get('height_m') or None
            age_estimate = request.POST.get('age_estimate') or None
            latitude = request.POST.get('latitude')
            longitude = request.POST.get('longitude')

            tree = TreeProfile.objects.create(
                street_name=street_name,
                scientific_name=scientific_name,
                habitat=habitat,
                description=description,
                rarity_status=rarity_status,
                height_m=height_m,
                age_estimate=age_estimate,
                latitude=latitude,
                longitude=longitude,
                submitted_by=request.user
            )

            return JsonResponse({
                'success': True,
                'street_name': tree.street_name,
                'latitude': float(tree.latitude),
                'longitude': float(tree.longitude),
                'description': tree.description or ''
            })

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request'})

# Dashboard
@login_required
def dashboard(request):
    pending_count = TreeRequest.objects.filter(status='pending').count()
    answered_week_count = TreeRequest.objects.filter(status='answered', created_at__gte=timezone.now()-timezone.timedelta(days=7)).count()
    trees_added_count = ... # implement per your tree model
    total_contributions = ... # e.g. answers by this user if contributor
    recent_activity = TreeRequest.objects.order_by('-created_at')[:6]
    context = {
       'pending_count': pending_count,
       'answered_week_count': answered_week_count,
       'trees_added_count': trees_added_count,
       'total_contributions': total_contributions,
       'recent_activity': recent_activity,
       # include my_requests, all_requests, my_answers etc as you already do
    }
    return render(request, 'Request/dashboard.html', context)


@login_required
def request_list(request):
    requests = TreeRequest.objects.all().order_by('-created_at')
    return render(request, "Request/request_list.html", {"requests": requests})

@login_required
def request_create(request):
    if request.method == "POST":
        form = TreeRequestForm(request.POST)
        if form.is_valid():
            new_request = form.save(commit=False)
            new_request.requester = request.user
            new_request.save()
            return redirect("request_list")  # Go back to request list
    else:
        form = TreeRequestForm()

    return render(request, "Request/request_form.html", {"form": form, "action": "Create"})

@login_required
def request_detail(request, pk):
    tr = get_object_or_404(TreeRequest, pk=pk)
    return render(request, "Request/request_detail.html", {"request_obj": tr})

@login_required
def request_edit(request, pk):
    tr = get_object_or_404(TreeRequest, pk=pk)
    if request.user != tr.requester:
        return JsonResponse({"error": "Permission denied"}, status=403)

    if request.method == "POST":
        form = TreeRequestForm(request.POST, instance=tr)
        if form.is_valid():
            form.save()
            return redirect("request_list")
    else:
        form = TreeRequestForm(instance=tr)
    return render(request, "Request/request_form.html", {"form": form})

@login_required
def request_delete(request, pk):
    tr = get_object_or_404(TreeRequest, pk=pk)
    if request.user != tr.requester:
        return JsonResponse({"error": "Permission denied"}, status=403)
    tr.delete()
    return redirect("request_list")

@login_required
def request_detail(request, pk):
    tr = get_object_or_404(TreeRequest, pk=pk)
    return render(request, "Request/request_detail.html", {"request_obj": tr})










# Ajax to create a new request
@login_required
@require_POST
def ajax_create_request(request):
    if request.user.user_type != "common":
        return JsonResponse({"success": False, "error": "Permission denied"}, status=403)

    form = TreeRequestForm(request.POST, request.FILES)
    if form.is_valid():
        tree_request = form.save(commit=False)
        tree_request.requester = request.user
        tree_request.save()

        # ✅ Save multiple uploaded images
        for file in request.FILES.getlist("images"):
            RequestImage.objects.create(tree_request=tree_request, image=file)

        return JsonResponse({"success": True})
    else:
        return JsonResponse({"success": False, "errors": form.errors}, status=400)

# Ajax to update an existing request
@login_required
@require_POST
def ajax_update_request(request, request_id):
    if request.user.user_type != "common":
        return JsonResponse({"success": False, "error": "Permission denied"}, status=403)

    tree_request = TreeRequest.objects.filter(id=request_id, requester=request.user).first()
    if not tree_request:
        return JsonResponse({"success": False, "error": "Request not found"})

    form = TreeRequestForm(request.POST, request.FILES, instance=tree_request)
    if form.is_valid():
        updated_request = form.save()

        # ✅ Add new uploaded images (if any)
        for file in request.FILES.getlist("images"):
            RequestImage.objects.create(tree_request=updated_request, image=file)

        return JsonResponse({"success": True})
    else:
        return JsonResponse({"success": False, "errors": form.errors}, status=400)

# Ajax to delete a request
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

def TreeDetail(request, id):
    tree = get_object_or_404(TreeProfile, id=id)

    return render(request, 'Trees/TreeDetail.html', {'tree': tree})

def map_page(request):
    return render(request, 'map.html')
