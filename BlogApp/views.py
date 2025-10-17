from django.shortcuts import render, get_object_or_404, redirect
from .models import BlogPost , Comment
from MyApp.models import User
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import BlogPostForm

# Create your views here.
def is_contributor(user):
    return user.user_type == 'contributor'
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
@login_required
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
# Add a blog post
@login_required
def add_blog(request):
    if not is_contributor(request.user):
        messages.error(request, "Only contributors can add blog posts.")
        return redirect('blog_list')
    
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            messages.success(request, "Blog post added successfully!")
            return redirect('blog_list')
    else:
        form = BlogPostForm()
    
    return render(request, 'blog/add_edit_blog.html', {'form': form, 'action': 'Add'})
# Edit a blog post
@login_required
def edit_blog(request, pk):
    blog = get_object_or_404(BlogPost, pk=pk)

    if not is_contributor(request.user):
        messages.error(request, "Only contributors can edit blog posts.")
        return redirect('blog_list')

    if request.user != blog.author:
        messages.error(request, "You can only edit your own posts.")
        return redirect('blog_list')

    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            messages.success(request, "Blog post updated successfully!")
            return redirect('blog_list')
    else:
        form = BlogPostForm(instance=blog)

    return render(request, 'blog/add_edit_blog.html', {'form': form, 'action': 'Edit'})

# Delete a blog post
@login_required
def delete_blog(request, pk):
    blog = get_object_or_404(BlogPost, pk=pk)

    if not is_contributor(request.user):
        messages.error(request, "Only contributors can delete blog posts.")
        return redirect('blog_list')

    if request.user != blog.author:
        messages.error(request, "You can only delete your own posts.")
        return redirect('blog_list')

    if request.method == 'POST':
        blog.delete()
        messages.success(request, "Blog post deleted successfully!")
    
    # Redirect back to blog list in any case
    return redirect('blog_list')


@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)
    if request.method == "POST":
        content = request.POST.get("content")
        comment.content = content
        comment.save()
        return redirect('blog_detail', pk=comment.post.pk)
    return render(request, 'blog/edit_comment.html', {'comment': comment})
@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('blog_detail', pk=post_pk)
