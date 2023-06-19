from django.shortcuts import render, redirect
from blog.decorators import login_required
from django.db.models import Q
from .models import Article
from .forms import ArticleForm
from comments.forms import CommentForm
# Create your views here.

from informations.utils import log_addition, log_change, log_deletion, inform_sb

def have_permission(request, article):
    return request.user==article.author.user or request.user.is_superuser

@login_required
def article_create_view(request):
    if request.method=="GET":
        form = ArticleForm(data=None)
    elif request.method=="POST":
        form = ArticleForm(data=request.POST)
        if form.is_valid():
            article=form.save(commit=False)
            article.author=request.user.account
            article.save()
            
            for account in request.user.account.follower.all():
                inform_sb(account, request.user.account, {"type": "article", "action": "create", "extra": article.id })
            log_addition(request, article, f"创建文章 {article.id}")

            return redirect(article.get_absolute_url())
        
    return render(request, "articles/edit.html", {"mode": "Create", "form": form})

def article_detail_view(request, slug):

    article = Article.objects.get(slug=slug)
    
    comment_form = CommentForm(data=None)
    
    context={
        "article": article,
        "comment_form": comment_form
    }
    return render(request, "articles/detail.html", context)

def article_search_view(request):
    query=request.GET.get("q")
    seach_type=request.GET.get("type")
    if query:
        if seach_type=="All":
            articles = Article.objects.filter(
                Q(title__icontains=query) | Q(content__icontains=query)
            )
        elif seach_type=="Title":
            articles = Article.objects.filter(
                Q(title__icontains=query)
            )
        elif seach_type=="Content":
            articles = Article.objects.filter(
                Q(content__icontains=query)
            )
        elif seach_type=="Author":
            articles = Article.objects.filter(
                Q(author__user__username__icontains=query)
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
                
                for account in request.user.account.follower.all():
                    inform_sb(account, request.user.account, {"type": "article", "action": "edit", "extra": article.id })
                log_change(request, article, f"修改文章 {article.id}")

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
                log_deletion(request, article, f"删除文章 {article.id}")
                article.delete()
                return redirect("home")
            else:
                return redirect(article.get_absolute_url())
    else:
        return render(request, "alert.html", {"message": "You do not have permission to delete!"})

@login_required
def article_vote_view(request, slug):
    # article和comment那边一模一样，修改时请注意两边都要修改
    if request.method == "POST":
        article = Article.objects.get(slug=slug)
        
        voting=request.POST.get("voting")
        if voting == "up_0":
            article.upvotes.remove(request.user.account)
            log_change(request, article, f"取消点赞文章 {article.id}")
        
        elif voting == "up_1":
            if request.user.account in article.downvotes.all():
                article.downvotes.remove(request.user.account)
            article.upvotes.add(request.user.account)
            for account in request.user.account.follower.all():
                if account!=article.author:
                    inform_sb(account, request.user.account, {"type": "article", "action": "upvote", "extra": article.id })
            inform_sb(article.author, request.user.account, {"type": "article", "action": "upvote", "extra": article.id })
            log_change(request, article, f"点赞文章 {article.id}")
        
        elif voting == "down_0":
            article.downvotes.remove(request.user.account)
            log_change(request, article, f"取消点踩文章 {article.id}")
        
        elif voting == "down_1":
            if request.user.account in article.upvotes.all():
                article.upvotes.remove(request.user.account)
            article.downvotes.add(request.user.account)
            log_change(request, article, f"点踩文章 {article.id}")
        
        if request.htmx:
            return render(request, "vote_btn.html", {"thing": article})
