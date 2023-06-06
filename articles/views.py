from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required #需要登陆才能用，会跳转到settings中的LOGIN_URL
from django.db.models import Q
from .models import Article
from .forms import ArticleForm
# Create your views here.

def article_search_view(request):
    query=request.GET.get("q")
    if query:
        articles = Article.objects.filter( Q(title__contains=query) | Q(content__contains=query) )
    else:
        articles = None
    context={
        "q": query,
        "articles": articles
    }
    return render(request, "articles/search.html", context)

@login_required
def article_create_view(request):
    form = ArticleForm(request.POST or None)
    context={
        "form": form
    }
    if form.is_valid():
        article=form.save()
        return redirect(article.get_absolute_url())
    else:
        return render(request, "articles/create.html", context)

def article_view(request, slug):
    article = Article.objects.get(slug=slug)
    context={
        "article": article
    }
    return render(request, "articles/detail.html", context)
