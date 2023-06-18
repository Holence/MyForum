from django.shortcuts import render
from django.db.models import Q
from blog.decorators import login_required

from accounts.models import Account
from .models import Messenger
from .forms import MessengerForm

# Create your views here.
@login_required
def messenger_view(request):
    me = request.user.account
    
    # message_dict，键为有消息的account，值为未读消息的个数
    message_dict={}
    for message in me.sent_messages.all():
        if not message_dict.get(message.receiver):
            message_dict[message.receiver]=0
    
    for message in me.received_messages.all():
        if not message_dict.get(message.sender):
            message_dict[message.sender]=0
        if message.read==False:
            message_dict[message.sender]+=1
    
    context = {
        "message_dict": message_dict
    }
    return render(request, "messenger/messenger.html", context)

@login_required
def messenger_messagesbox_view(request):
    if request.method == "POST":
        receiver_username = request.POST.get("account")
        form = MessengerForm(data=None)

        sender = Account.objects.get(user__username=request.user.username)
        receiver = Account.objects.get(user__username=receiver_username)

        messages = Messenger.objects.filter(
            (Q(sender=sender) & Q(receiver=receiver)) | (Q(sender=receiver) & Q(receiver=sender))
        )
        return render(request, "messenger/messages_box.html", {"form": form, "messages": messages, "account": receiver})

@login_required
def messenger_post_view(request):
    if request.method == "POST":
        receiver_username = request.POST.get("account")
        
        sender = Account.objects.get(user__username=request.user.username)
        receiver = Account.objects.get(user__username=receiver_username)

        form = MessengerForm(data=request.POST)
        
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.receiver = receiver
            message.save()

        form = MessengerForm(data=None)
        messages = Messenger.objects.filter(
            (Q(sender=sender) & Q(receiver=receiver)) | (Q(sender=receiver) & Q(receiver=sender))
        )

        return render(request, "messenger/messages_box.html", {"form": form, "messages": messages, "account": receiver})
