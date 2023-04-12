from django.shortcuts import render, redirect, get_object_or_404

from django.http import HttpResponse

from django.contrib.auth.models import User

from django.core.paginator import Paginator

from .models import Category, Post, Tag
from .forms import PostForm

import markdown, re

# Create your views here.
def index(request):
    post = Post.objects.all()
    # 每页显示文章条目数
    paginator = Paginator(post, 4)
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    context  = { 'articles': articles }
    return render(request, 'article/index.html', context)

def detail(request, pk):
    article = Post.objects.get(pk=pk)
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
        ])
    article.body = md.convert(article.body)
    # 正则判断是否有目录
    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    article.toc = m.group(1) if m is not None else ''
    context = { 'article': article}
    return render(request, 'article/detail.html', context)

def archive(request, year, month):
    articles = Post.objects.filter(created__year=year, created__month=month)
    return render(request, 'article/index.html', context={'articles': articles})

def category(request, pk):
    cate = get_object_or_404(Category, pk=pk)
    articles = Post.objects.filter(category=cate)
    return render(request, 'article/index.html', context={'articles': articles})

def tag(request, pk):
    t = get_object_or_404(Tag, pk=pk)
    articles = Post.objects.filter(tags=t)
    return render(request, 'article/index.html', context={'articles': articles})

def delete(request, pk):
    if request.method == 'POST':
        article = Post.objects.get(pk=pk)
        article.delete()
        return redirect("article:index")
    else:
        return HttpResponse("ERROR! Request post only!")

def create(request):
    if request.method == "POST":
        post_form = PostForm(data=request.POST)
        if post_form.is_valid():
            new_article = post_form.save(commit=False)
            new_article.author = User.objects.get(pk=1)
            new_article.save()
            return redirect("article:index")
        else:
            return HttpResponse("ERROR!")
    else:
        post_form = PostForm()
        context = { 'post_form': post_form }
        return render(request, 'article/create.html', context)

def update(request, pk):
    article = Post.objects.get(pk=pk)
    if request.method == "POST":
        post_form = PostForm(data=request.POST)
        if post_form.is_valid():
            article.title = request.POST['title']
            article.body = request.POST['body']
            article.save()
            return redirect("article:detail", pk=pk)
        else:
            return HttpResponse("ERROR!")
    else:
        post_form = PostForm()
        context = { 'article':article, 'post_form': post_form }
        return render(request, 'article/update.html', context)

