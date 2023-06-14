from django.shortcuts import render, redirect
from blog.decorators import login_required
from articles.models import Article
from .models import Comment
from .forms import CommentForm

# Create your views here.
def have_permission(request, comment):
    return request.user==comment.author.user or request.user.is_superuser

@login_required
def comment_post_view(request):
    if request.method=="POST":
        article_slug = request.POST.get("article_slug")
        article = Article.objects.get(slug=article_slug)
        reply_to_id = request.POST.get("reply_to_id")
        if reply_to_id!="None":
            reply_to = Comment.objects.get(id=int(reply_to_id))
        else:
            reply_to = None
        
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user.account
            comment.article = article
            comment.reply_to = reply_to
            comment.save()
            return redirect(comment.get_absolute_url())

@login_required
def comment_reply_view(request):
    comment_form = CommentForm(data=None)
    article_slug = request.POST.get("article_slug")
    reply_to_id = request.POST.get("reply_to_id")
    
    context={
        "comment_form": comment_form,
        "article_slug": article_slug,
        "reply_to_id": reply_to_id,
    }
    if request.htmx:
        return render(request, "comments/edit.html", context)

@login_required
def comment_delete_view(request, id):
    comment = Comment.objects.get(id=id)
    article = comment.article
    if have_permission(request, comment):
        if request.method=="GET":
            return render(request, "delete.html", {})
        if request.method=="POST":
            choice=request.POST.get("choice")
            if choice=="Yes":
                comment.content=None
                comment.save()
            return redirect(article.get_absolute_url())
    else:
        return render(request, "alert.html", {"message": "You do not have permission to delete!"})

@login_required
def comment_vote_view(request, id):
    # article和comment那边一模一样，修改时请注意两边都要修改
    comment = Comment.objects.get(id=id)

    voting=request.POST.get("voting")
    if voting == "up_0":
        comment.upvotes.remove(request.user.account)
    elif voting == "up_1":
        if request.user.account in comment.downvotes.all():
            comment.downvotes.remove(request.user.account)
        comment.upvotes.add(request.user.account)
    elif voting == "down_0":
        comment.downvotes.remove(request.user.account)
    elif voting == "down_1":
        if request.user.account in comment.upvotes.all():
            comment.upvotes.remove(request.user.account)
        comment.downvotes.add(request.user.account)
    
    if request.htmx:
        return render(request, "vote_btn.html", {"thing": comment})
