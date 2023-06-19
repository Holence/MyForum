from django.shortcuts import render
from django.db.models import Q
from blog.decorators import login_required

from accounts.models import Account
from .models import Messenger
from .forms import MessengerForm

from informations.utils import log_addition, log_change, log_deletion, inform_sb

# Create your views here.
@login_required
def messenger_view(request):
    
    me = request.user.account
    
    # messenger_dict，键为有消息的account，值为未读消息的个数
    messenger_dict={}
    for message in me.sent_messages.all():
        if not messenger_dict.get(message.receiver):
            messenger_dict[message.receiver]=0
    
    for message in me.received_messages.all():
        if not messenger_dict.get(message.sender):
            messenger_dict[message.sender]=0
        if message.read==False:
            messenger_dict[message.sender]+=1

    messenger_dict=dict(sorted(messenger_dict.items(), key = lambda x:x[0].user.username))

    if request.htmx:
        # current_ta 是 定时刷新 之前选中的
        current_ta=request.GET.get("current_ta")
        if current_ta:
            current_ta=Account.objects.get(user__username=current_ta)
            if current_ta not in messenger_dict.keys():
                messenger_dict[current_ta]=-1
        return render(request, "messenger/messenger_list.html", {"messenger_dict": messenger_dict, "current_ta": current_ta})
    else:
        # current_ta 是 点私信按钮进来的
        # 如果点Messenger进来，是没有这个参数的
        current_ta=request.GET.get("current_ta")
        if current_ta:
            current_ta=Account.objects.get(user__username=current_ta)
            if current_ta not in messenger_dict.keys():
                messenger_dict[current_ta]=-1
        return render(request, "messenger/base.html", {"messenger_dict": messenger_dict, "current_ta": current_ta})

@login_required
def messenger_messagesbox_view(request):
    me = request.user.account

    if request.method == "GET":
        receiver_username = request.GET.get("account")
        ta = Account.objects.get(user__username=receiver_username)

        for message in Messenger.objects.filter(Q(sender=ta) & Q(receiver=me)).all():
            message.read=True
            message.save()

    if request.method == "POST":
        receiver_username = request.POST.get("account")
        ta = Account.objects.get(user__username=receiver_username)

        form = MessengerForm(data=request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = me
            message.receiver = ta
            message.save()
            log_addition(request, message, f"发送私信 {message.id}")

    form = MessengerForm(data=None)
    messages = Messenger.objects.filter(
        (Q(sender=me) & Q(receiver=ta)) | (Q(sender=ta) & Q(receiver=me))
    ).order_by("timestamp")

    return render(request, "messenger/messages_box.html", {"form": form, "messages": messages, "account": ta})

@login_required
def messenger_messageslist_view(request):
    if request.method == "GET":
        receiver_username = request.GET.get("account")

        me = request.user.account
        ta = Account.objects.get(user__username=receiver_username)

        for message in Messenger.objects.filter(Q(sender=ta) & Q(receiver=me)).all():
            message.read=True
            message.save()

        messages = Messenger.objects.filter(
            (Q(sender=me) & Q(receiver=ta)) | (Q(sender=ta) & Q(receiver=me))
        ).order_by("timestamp")
        return render(request, "messenger/messages_list.html", {"messages": messages, "account": ta})
