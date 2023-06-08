from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Comment
# Create your views here.
def have_permission(request, comment):
    return request.user==comment.user or request.user.is_superuser

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
