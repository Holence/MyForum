from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Comment
# Create your views here.
def have_permission(request, comment):
    return request.user==comment.author.user or request.user.is_superuser

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
                comment.delete()
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
