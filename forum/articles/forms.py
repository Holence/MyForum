from django import forms
from .models import Article
from martor.fields import MartorFormField

class ArticleForm(forms.ModelForm):
    content = MartorFormField()
    class Meta:
        model = Article
        fields = ["title", "content"]

    # 直接在model中设置title为unique就行了
    # def clean(self):
    #     data=super().clean()
    #     title = data.get("title")
    #     qs = Article.objects.filter(title__exact=title)
    #     if qs:
    #         self.add_error("title", f"\"{title}\" is already in use.")
        
    #     return data
