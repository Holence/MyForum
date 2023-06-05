from django import forms
from .models import Article

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title", "content"]

    def clean(self):
        data=super().clean()
        title = data.get("title")
        qs = Article.objects.filter(title__exact=title)
        print(qs)
        if qs:
            self.add_error("title", f"\"{title}\" is already in use.")
        
        return data
