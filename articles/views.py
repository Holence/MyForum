from django.shortcuts import render
from django.contrib.auth.decorators import login_required #需要登陆才能用，会跳转到settings中的LOGIN_URL

from .models import Article
from .forms import ArticleForm
# Create your views here.

def article_search_view(request):
    query=request.GET.get("q")
    if query:
        articles = Article.objects.filter(content__contains=query)
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
    print(form.is_valid())
    if form.is_valid():
        article=form.save()
        context["article"] = article
        context["created"] = True
    return render(request, "articles/create.html", context)

def article_view(request, id):
    
    article = Article.objects.get(id=id)
    context={
        "article": article
    }
    return render(request, "articles/detail.html", context)