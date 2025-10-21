from django.shortcuts import render, get_object_or_404, redirect
from .models import BlogPost , Comment, Notification , Bookmark
from MyApp.models import User
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import BlogPostForm
from django.http import JsonResponse
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

    # Always define bookmarked
    bookmarked = False
    if request.user.is_authenticated:
        bookmarked = post.bookmarked_by.filter(user=request.user).exists()

    if request.method == "POST":
        content = request.POST.get("content")
        parent_id = request.POST.get("parent_id")
        parent_comment = Comment.objects.filter(id=parent_id).first() if parent_id else None

        # create the comment
        comment = Comment.objects.create(post=post, user=request.user, content=content, parent=parent_comment)

        # create notifications
        if post.author and post.author != request.user:
            Notification.objects.create(
                recipient=post.author,
                sender=request.user,
                notif_type='comment',
                post=post,
                comment=comment,
                message=f"{request.user.username} commented on your post '{post.title}'."
            )

        if parent_comment and parent_comment.user != request.user:
            Notification.objects.create(
                recipient=parent_comment.user,
                sender=request.user,
                notif_type='reply',
                post=post,
                comment=comment,
                message=f"{request.user.username} replied to your comment on '{post.title}'."
            )

        return redirect("blog_detail", pk=pk)

    return render(request, "blog/blog_detail.html", {
        "post": post,
        "comments": comments,
        "bookmarked": bookmarked,
    })


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




def add_comment(request, post_id):
    post = BlogPost.objects.get(id=post_id)
    comment = Comment.objects.create(
        post=post,
        user=request.user,
        content=request.POST.get('content')
    )

    # Notify the post author if they are not the commenter
    if post.author != request.user:
        Notification.objects.create(
            recipient=post.author,
            sender=request.user,
            notif_type='comment',
            post=post,
            comment=comment,
            message=f"{request.user.username} commented on your post '{post.title}'."
        )
    return redirect('post_detail', post_id=post.id)

def add_reply(request, comment_id):
    parent_comment = Comment.objects.get(id=comment_id)
    reply = Comment.objects.create(
        post=parent_comment.post,
        user=request.user,
        content=request.POST.get('content'),
        parent=parent_comment
    )

    # Notify the original commenter if they are not the replier
    if parent_comment.user != request.user:
        Notification.objects.create(
            recipient=parent_comment.user,
            sender=request.user,
            notif_type='reply',
            post=parent_comment.post,
            comment=reply,
            message=f"{request.user.username} replied to your comment on '{parent_comment.post.title}'."
        )
    return redirect('post_detail', post_id=parent_comment.post.id)

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

@login_required
def mark_notifications_read(request):
    if request.method == "POST":
        request.user.notifications.update(is_read=True)
        return JsonResponse({"success": True})
    return JsonResponse({"success": False}, status=400)


@login_required
def mark_single_notification_read(request, notif_id):
    if request.method == "POST":
        notif = request.user.notifications.filter(id=notif_id).first()
        if notif:
            notif.is_read = True
            notif.save()
            return JsonResponse({"success": True})
    return JsonResponse({"success": False}, status=400)


@login_required
def toggle_bookmark(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    bookmark, created = Bookmark.objects.get_or_create(user=request.user, post=post)
    if not created:
        bookmark.delete()  # remove bookmark
    return JsonResponse({"success": True, "bookmarked": created})

@login_required
def bookmark_post(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    
    # toggle bookmark
    if post.bookmarked_by.filter(user=request.user).exists():
        post.bookmarked_by.filter(user=request.user).delete()
        bookmarked = False
    else:
        post.bookmarked_by.create(user=request.user)
        bookmarked = True

    return JsonResponse({"bookmarked": bookmarked})