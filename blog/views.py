from django.shortcuts import render, get_object_or_404
from .models import Post, Category, Tag
from sk_pro import helpers
from django.db.models import Count



def post_list(request, category_slug=None, tag_slug=None):
    post_list = Post.objects.all().order_by('-publish')
    posts = helpers.pg_records(request, post_list, 2)

    category = None
    categories = Category.objects.all().order_by('-publish')

    tag = None
    object_list = Post.objects.all().order_by('-publish')

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = object_list.filter(tags__in=[tag])
        posts = helpers.pg_records(request, post_list, 2)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        post_list = post_list.filter(category=category)
        posts = helpers.pg_records(request, post_list, 2)

    return render(request, 'blog/post/list.html', {'posts': posts,
                                                   'category': category,
                                                   'categories': categories,
                                                   'tag': tag})


def search(request):
    if 'q' in request.GET:
        q = request.GET['q']
        post_list = Post.objects.filter(title__icontains=q)
        posts = helpers.pg_records(request, post_list, 2)

        return render(request, 'blog/post/search.html', {'posts': posts, 'q': q})


def post_detail(request, post):
    post = get_object_or_404(Post, slug=post)

    # List of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.objects.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:3]

    return render(request,'blog/post/detail.html', {'post': post,
                                                    'similar_posts': similar_posts})