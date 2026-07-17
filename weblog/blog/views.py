from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.utils.text import slugify
from django.views.decorators.http import require_POST
from .models import Post, Category, Tag, comment as Comment


def home(request):
    if request.method == 'POST':
        post = Post.objects.create(
            title=request.POST.get('title'),
            slug=slugify(request.POST.get('title', ''))[:30] or f"post-{timezone.now().timestamp()}",
            body=request.POST.get('body'),
            author_id=1,
            image=request.FILES.get('image'),
            published=True,
            created_at=timezone.now(),
            updated_at=timezone.now(),
        )

        cat_id = request.POST.get('category')
        new_cat_name = request.POST.get('new_category', '').strip()
        if new_cat_name:
            cat, _ = Category.objects.get_or_create(
                name=new_cat_name, defaults={'slug': slugify(new_cat_name)}
            )
            post.category.add(cat)
        elif cat_id:
            post.category.add(cat_id)

        tag_ids = request.POST.getlist('tags')
        if tag_ids:
            post.tags.set(tag_ids)
        new_tag_name = request.POST.get('new_tag', '').strip()
        if new_tag_name:
            tag, _ = Tag.objects.get_or_create(
                name=new_tag_name, defaults={'slug': slugify(new_tag_name)}
            )
            post.tags.add(tag)

        return redirect('home')

    return render(request, 'accounts/home.html', {
        'posts': Post.objects.filter(published=True).order_by('-created_at'),
        'categories': Category.objects.all(),
        'tags': Tag.objects.all(),
    })


@require_POST
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    text = (request.POST.get('text') or '').strip()
    if text:
        Comment.objects.create(
            post=post,
            author=(request.POST.get('author') or '').strip() or 'anonymous',
            body=text,
            created_at=timezone.now(),
        )
    return redirect('home')


@require_POST
def delete_post(request, post_id):
    get_object_or_404(Post, id=post_id).delete()
    return redirect('home')


def category_posts(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    return render(request, 'accounts/home.html', {
        'posts': Post.objects.filter(published=True, category=category).order_by('-created_at'),
        'categories': Category.objects.all(),
        'tags': Tag.objects.all(),
        'active_category': category,
    })


def tag_posts(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)
    return render(request, 'accounts/home.html', {
        'posts': Post.objects.filter(published=True, tags=tag).order_by('-created_at'),
        'categories': Category.objects.all(),
        'tags': Tag.objects.all(),
        'active_tag': tag,
    })