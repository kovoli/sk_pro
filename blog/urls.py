from django.conf.urls import url
from . import views


app_name = 'blog'

urlpatterns = [
    # post views
    url(r'^$', views.post_list, name='post_list'),
    url(r'(?P<post>[-\w]+)/$', views.post_detail, name='post_detail'),
]
