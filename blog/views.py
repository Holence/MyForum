from django.shortcuts import render
from articles.models import Article

def home_view(request):
    article_queryset = Article.objects.all()
    context={
        "article_queryset": article_queryset
    }
    return render(request, "home_view.html", context)
