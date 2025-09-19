from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from .models import BlogPost , Comment
from django.core.paginator import Paginator

# Create your views here.
# blog_views
def blog_list(request):
    posts = BlogPost.objects.order_by('-date_posted')
    featured = posts.first()  # Latest post
    others = posts[1:]

    paginator = Paginator(others, 6)  # 6 posts at a time
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog/blog_list.html', {
        'featured': featured,
        'page_obj': page_obj
    })
# Detail view
def blog_detail(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    comments = post.comments.filter(parent__isnull=True)

    if request.method == "POST":
        content = request.POST.get("content")
        parent_id = request.POST.get("parent_id")
        parent_comment = Comment.objects.filter(id=parent_id).first() if parent_id else None
        Comment.objects.create(post=post, user=request.user, content=content, parent=parent_comment)
        return redirect("blog_detail", pk=pk)

    return render(request, "blog/blog_detail.html", {"post": post, "comments": comments})