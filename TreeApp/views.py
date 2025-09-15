from django.shortcuts import render
from .models import *

# Create your views here.

def TreeProfiles(request):

    TreeProfiles = TreeProfile.objects.all()
    
    context = {
            'TreeProfiles': TreeProfiles
        }
    print(TreeProfiles)  
    return render(request, 'Trees/TreeProfiles.html', context=context)
