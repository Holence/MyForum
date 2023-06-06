from django.test import TestCase

# Create your tests here.
from .models import Article

class ArticleTestCase(TestCase):
    def setUp(self) -> None:
        for i in range(5):
            Article.objects.create(title="Test Case %s"%i, content="A test article.")

    def test_queryset_exist(self):
        qs = Article.objects.all()
        self.assertIsNotNone(qs)