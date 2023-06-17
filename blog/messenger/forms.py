from django import forms
from .models import Messenger
from martor.fields import MartorFormField

class MessengerForm(forms.ModelForm):
    content = MartorFormField()
    class Meta:
        model = Messenger
        fields = ["content"]
