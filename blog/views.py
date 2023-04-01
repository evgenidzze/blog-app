from django.shortcuts import render
from django.views.generic import ListView, DetailView

from blog.models import Post


class BlogListView(ListView):
    model = Post
    template_name = 'home.html'
    context_object_name = 'blog_posts'


class BlogDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'detail_post'