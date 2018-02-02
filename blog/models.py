from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    author = models.ForeignKey(User, default=User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:posts_by_category', args=[self.slug])

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    author = models.ForeignKey(User, default=User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
       return self.name

    def get_absolute_url(self):
        return reverse('blog:posts_by_tag', args=[self.slug])

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, related_name='blog_posts', on_delete=models.SET_NULL, null=True)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField(Tag)
    image = models.ImageField(upload_to='post_image/%Y/%m/', blank=True)
    image_post = ImageSpecField(source='image',
                                processors=[ResizeToFill(900, 600)],
                                format='JPEG',
                                options={'quality': 50})
    image_sidebar = ImageSpecField(source='image',
                                   processors=[ResizeToFill(80, 80)],
                                   format='JPEG',
                                   options={'quality': 50})
    image_list = ImageSpecField(source='image',
                                processors=[ResizeToFill(600, 400)],
                                format='JPEG',
                                options={'quality': 50})

    class Meta:
        ordering = ('-publish',)
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.slug])

