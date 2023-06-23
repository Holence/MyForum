from django.shortcuts import render
from accounts.models import Account
from articles.models import Article
from comments.models import Comment

name_dict={
    "follow": "关注了你",
    
    "create": "发表了",
    "reply": "回复了",
    "edit": "修改了",
    "upvote": "点赞了",
    
    "article": "文章",
    "comment": "评论",
}

# Create your views here.
def informations_view(request):
    # 跟依托答辩一样
    informations = request.user.account.user_informations.all().order_by("-timestamp")
    informations_list=[]
    for information in informations:
        timestamp = information.timestamp
        info = information.info
        account_id = info["who"]
        account = Account.objects.get(id=account_id)
        type = name_dict.get(info["type"], "")
        action = name_dict[info["action"]]
        thing=None
        if info["type"]=="article":
            thing = Article.objects.get(id=info["extra"])
            if request.user.account==thing.author:
                    action+="你的"
        if info["type"]=="comment":
            thing = Comment.objects.get(id=info["extra"])
            if info["action"]=="reply":
                if thing.reply_to==None:
                    type=name_dict["article"]
                    if request.user.account==thing.article.author:
                        action+="你的"
                else:
                    if request.user.account==thing.reply_to.author:
                        action+="你的"
            if info["action"]=="upvote":
                if request.user.account==thing.author:
                    action+="你的"
        
        informations_list.append({
            "timestamp": timestamp,
            "account": account,
            "action": action,
            "type": type,
            "thing": thing,
            "read": information.read,
        })
        information.read=True
        information.save()
        
    return render(request, "informations/base.html", {"informations_list": informations_list})