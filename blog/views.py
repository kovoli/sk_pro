from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



def post_list(request):
    object_list = Post.objects.all()
    paginator = Paginator(object_list, 2)
    page = request.GET.get('page')
    try:
        posts =paginator.page(page)
    except PageNotAnInteger:
        # Если страница не является целым числом, доставьте первую страницу
        posts = paginator.page(1)
    except EmptyPage:
        # Если страница за пределами допустимого диапазона доставляет последнюю страницу результатов
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/post/list.html', {'page': page, 'posts': posts})


def post_detail(request, post):
    post = get_object_or_404(Post, slug=post)
    return render(request, 'blog/post/detail.html', {'post': post})