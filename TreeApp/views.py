from django.shortcuts import render, redirect
from .models import *
from .forms import *
import json
from django.core.serializers.json import DjangoJSONEncoder

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
