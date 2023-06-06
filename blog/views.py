from django.shortcuts import render
from articles.models import Article

def home_view(request):
    articles = Article.objects.all()
    context={
        "articles": articles
    }
    return render(request, "home_view.html", context)
