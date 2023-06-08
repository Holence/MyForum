from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required #需要登陆才能用，会跳转到settings中的LOGIN_URL
from django.db.models import Q
from .models import Article
from .forms import ArticleForm
from comments.forms import CommentForm
# Create your views here.

def have_permission(request, article):
    return request.user==article.author or request.user.is_superuser

@login_required
def article_create_view(request):
    if request.method=="GET":
        form = ArticleForm(data=None)
    elif request.method=="POST":
        form = ArticleForm(data=request.POST)
        if form.is_valid():
            article=form.save(commit=False)
            article.author=request.user
            article.save()
            return redirect(article.get_absolute_url())
        
    return render(request, "articles/edit.html", {"mode": "Create", "form": form})

def article_detail_view(request, slug):

    article = Article.objects.get(slug=slug)
        
    if request.method=="GET":
        form = CommentForm(data=None)
        
    elif request.method=="POST":
        if request.user.is_authenticated:
            form = CommentForm(data=request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.user = request.user
                comment.article = article
                comment.save()
                return redirect(article.get_absolute_url())
        else:
            return redirect("login")
    
    context={
        "article": article,
        "form": form
    }
    return render(request, "articles/detail.html", context)
    

def article_search_view(request):
    query=request.GET.get("q")
    seach_type=request.GET.get("type")
    if query:
        if seach_type=="all":
            articles = Article.objects.filter(
                Q(title__icontains=query) | Q(content__icontains=query)
            )
        elif seach_type=="title":
            articles = Article.objects.filter(
                Q(title__icontains=query)
            )
        elif seach_type=="content":
            articles = Article.objects.filter(
                Q(content__icontains=query)
            )
    else:
        articles = None
    context={
        "query": query,
        "articles": articles
    }
    if request.htmx:
        return render(request, "articles/search_list.html", context)
    else:
        return render(request, "articles/search.html", context)

@login_required
def article_edit_view(request, slug):
    article = Article.objects.get(slug=slug)
    if have_permission(request, article):
        if request.method=="GET":
            form = ArticleForm(data=None, instance=article)
        elif request.method=="POST":
            form = ArticleForm(data=request.POST, instance=article)
            if form.is_valid():
                form.save()
                return redirect(article.get_absolute_url())
        return render(request, "articles/edit.html", {"mode": "Edit", "form": form})
    else:
        return render(request, "alert.html", {"message": "You do not have permission to edit!"})

@login_required
def article_delete_view(request, slug):
    article = Article.objects.get(slug=slug)
    if have_permission(request, article):
        if request.method=="GET":
            return render(request, "delete.html", {})
        if request.method=="POST":
            choice=request.POST.get("choice")
            if choice=="Yes":
                article.delete()
                return redirect("home")
            else:
                return redirect(article.get_absolute_url())
    else:
        return render(request, "alert.html", {"message": "You do not have permission to delete!"})
