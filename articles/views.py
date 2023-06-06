from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required #需要登陆才能用，会跳转到settings中的LOGIN_URL
from django.db.models import Q
from .models import Article
from .forms import ArticleForm
# Create your views here.

def have_permission(request, article):
    return request.user==article.author or request.user.is_superuser

@login_required
def article_create_view(request):
    if request.method=="GET":
        form = ArticleForm()
    elif request.method=="POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            article=form.save(commit=False)
            article.author=request.user
            article.save()
            return redirect(article.get_absolute_url())
        
    return render(request, "articles/edit.html", {"mode": "Create", "form": form})

def article_detail_view(request, slug):
    article = Article.objects.get(slug=slug)
    context={
        "article": article
    }
    return render(request, "articles/detail.html", context)

def article_search_view(request):
    query=request.GET.get("q")
    if query:
        articles = Article.objects.filter(
            Q(title__contains=query) | Q(content__contains=query)
        )
    else:
        articles = None
    context={
        "q": query,
        "articles": articles
    }
    return render(request, "articles/search.html", context)

@login_required
def article_edit_view(request, slug):
    article = Article.objects.get(slug=slug)
    if have_permission(request, article):
        if request.method=="GET":
            form = ArticleForm(None, instance=article)
        elif request.method=="POST":
            form = ArticleForm(request.POST, instance=article)
            if form.is_valid():
                form.save()
                return redirect(article.get_absolute_url())
        return render(request, "articles/edit.html", {"mode": "Edit", "form": form, "alert": False})
    else:
        return render(request, "alert.html", {"message": "You do not have permission to edit!"})

@login_required
def article_delete_view(request, slug):
    article = Article.objects.get(slug=slug)
    if have_permission(request, article):
        if request.method=="GET":
            return render(request, "articles/delete.html", {})
        if request.method=="POST":
            choice=request.POST.get("choice")
            if choice=="Yes":
                article.delete()
                return redirect("/")
            else:
                return redirect(article.get_absolute_url())
    else:
        return render(request, "alert.html", {"message": "You do not have permission to delete!"})
