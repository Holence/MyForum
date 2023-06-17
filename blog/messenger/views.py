from django.shortcuts import render
from .models import Messenger
from accounts.models import Account
from django.db.models import Q
from .forms import MessengerForm

# Create your views here.
def messenger_view(request):
    messages = Messenger.objects.filter(sender=request.user.account)
    receivers = [i.receiver for i in messages]
    context = {
        "receivers": receivers
    }
    return render(request, "messenger/base.html", context)

def messenger_messages_view(request):
    receiver_username = request.POST.get("receiver")
    form = MessengerForm(data=None)

    sender = Account.objects.get(user__username=request.user.username)
    receiver = Account.objects.get(user__username=receiver_username)

    messages = Messenger.objects.filter(
        (Q(sender=sender) & Q(receiver=receiver)) | (Q(sender=receiver) & Q(receiver=sender))
    )
    print(messages)
    return render(request, "messenger/messages_list.html", {"form": form, "messages": messages})