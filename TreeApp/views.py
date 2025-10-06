from django.shortcuts import render, redirect
from .models import *
from .forms import *
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

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
