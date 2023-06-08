from django import forms
from django.core.files.images import get_image_dimensions

from .models import Account

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        exclude = ["user"]

    def clean_avatar(self):
        avatar = self.cleaned_data['avatar']

        if avatar:
            try:
                w, h = get_image_dimensions(avatar)

                #validate dimensions
                max_width = max_height = 2048
                if w > max_width or h > max_height:
                    raise forms.ValidationError(
                        u'Please use an image that is '
                        '%s x %s pixels or smaller.' % (max_width, max_height))

                #validate content type
                main, sub = avatar.content_type.split('/')
                if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'gif', 'png']):
                    raise forms.ValidationError(u'Please use a JPEG, '
                        'GIF or PNG image.')

                #validate file size
                if len(avatar) > (20 * 1024):
                    raise forms.ValidationError(
                        u'Avatar file size may not exceed 20k.')

            except AttributeError:
                """
                Handles case when we are updating the user profile
                and do not supply a new avatar
                """
                pass

        return avatar