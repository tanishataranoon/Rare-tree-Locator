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
from django.contrib import messages
from .models import TreeProfile

def is_contributor(user):
    # Option A: based on a custom user_type field
    return hasattr(user, 'user_type') and user.user_type == 'contributor'
    
    # Option B: based on group membership
    # return user.groups.filter(name="Contributors").exists()


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
    if not is_contributor(request.user):
        return JsonResponse({'success': False, 'error': 'Only contributors can add trees.'})

    if request.method == 'POST':
        try:
            # Tree info
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

            # Save uploaded photos
            photos = request.FILES.getlist('tree_photos')
            for photo in photos:
                TreePhoto.objects.create(tree=tree, image=photo)

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


def TreeDetail(request, id):
    tree = get_object_or_404(TreeProfile, id=id)

from django.shortcuts import render, get_object_or_404
from .models import TreeProfile

def tree_detail(request, pk):
    tree = get_object_or_404(TreeProfile, pk=pk)
    # convert Decimal to float for JS ease (optional but ভালো)
    try:
        lat = float(tree.latitude)
        lng = float(tree.longitude)
    except Exception:
        lat = None
        lng = None

    return render(request, 'Trees/TreeDetail.html', {
        'tree': tree,
        'tree_lat': lat,
        'tree_lng': lng,
    })

def map_page(request):
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
    trees_json = json.dumps(trees, cls=DjangoJSONEncoder)

    can_add_tree = is_contributor(request.user) if request.user.is_authenticated else False

    return render(request, 'map.html', {'trees_json': trees_json, 'can_add_tree': can_add_tree})


# Dashboard
@login_required
def dashboard(request):
    pending_count = TreeRequest.objects.filter(status='pending').count()
    answered_week_count = TreeRequest.objects.filter(
        status='answered',
        created_at__gte=timezone.now() - timezone.timedelta(days=7)
    ).count()

    # You can fill these later depending on your tree models
    trees_added_count = 0  
    total_contributions = 0

    recent_activity = TreeRequest.objects.order_by('-created_at')[:6]

    context = {
        'pending_count': pending_count,
        'answered_week_count': answered_week_count,
        'trees_added': trees_added_count,
        'total_contrib': total_contributions,
        'recent_activity': recent_activity,
    }
    return render(request, 'Dashboard/dashboard.html', context)

@login_required
def tree_requests(request):
    # Whatever logic you used in your old `request_list` view
    my_requests = TreeRequest.objects.filter(requester=request.user)
    all_requests = TreeRequest.objects.all().order_by('-created_at')

    context = {
        'my_requests': my_requests,
        'all_requests': all_requests,
    }
    return render(request, 'Dashboard/tree_requests.html', context)

@login_required
def request_list(request):
    requests = TreeRequest.objects.all().order_by("-created_at")
    form = TreeRequestForm()
    return render(request, "Dashboard/tree_requests.html", {"requests": requests, "form": form})


@login_required
def create_request(request):
    if request.method == "POST":
        form = TreeRequestForm(request.POST, request.FILES)
        if form.is_valid():
            tree_request = form.save(commit=False)
            tree_request.requester = request.user
            tree_request.save()
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"success": False, "errors": form.errors})
    return JsonResponse({"success": False, "error": "Invalid request"})

@login_required
def request_detail_ajax(request, pk):
    tree_request = get_object_or_404(TreeRequest, pk=pk)
    data = {
        "id": f"REQ-{tree_request.id:03}",
        "title": tree_request.title,
        "description": tree_request.description,
        "location": tree_request.location,
        "created_at": tree_request.created_at.strftime("%Y-%m-%d %H:%M"),
        "status": tree_request.get_status_display(),
        "requester": tree_request.requester.username,
        "image_url": tree_request.image.url if tree_request.image else "",
    }
    return JsonResponse(data)

@login_required
def delete_request(request, id):
    if request.method == 'POST':
        req = get_object_or_404(TreeRequest, id=id)
        if req.requester == request.user:
            req.delete()
            return JsonResponse({"success": True})
        return JsonResponse({"error": "Not authorized"}, status=403)
    return JsonResponse({"error": "Invalid method"}, status=400)




@login_required
def answer_request(request, pk):
    tree_request = get_object_or_404(TreeRequest, pk=pk)
    answers = tree_request.answers.all().order_by('-created_at')

    if request.method == "POST":
        form = TreeAnswerForm(request.POST, request.FILES)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.tree_request = tree_request
            answer.answered_by = request.user
            answer.save()
            return redirect('answer_request', pk=pk)
    else:
        form = TreeAnswerForm()

    return render(request, 'Request/answer_request.html', {
        'tree_request': tree_request,
        'answers': answers,
        'form': form,
    })


def view_submitted_answer(request, pk):
    tree_request = get_object_or_404(TreeRequest, pk=pk)
    answers = tree_request.answers.all().order_by("-created_at")

    return render(request, "Request/view_submitted_answer.html", {
        "tree_request": tree_request,
        "answers": answers
    })

# Contact form
def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")
        print("CONTACT MSG:", name, email, message)
        messages.success(request, "Thanks — your message was received!")
        return redirect('contact')
    return render(request, "contact.html")