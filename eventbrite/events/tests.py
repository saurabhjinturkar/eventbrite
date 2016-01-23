from django.test import TestCase
from django.test import Client
from models import Category


class CategoryTestCase(TestCase):
    def setUp(self):
        c = Category()
        c.name = 'test_category'
        c.category_id = 1
        c.save()

    def test_categories(self):
        test = Category.objects.get(pk=1)
        assert test.category_id, 1


class ViewTestCase(TestCase):
    def setUp(self):
        self.c = Client()

    def test_event_selection(self):
        response = self.c.get('/')
        assert response.status_code, 200

    def test_event_show(self):
        response = self.c.post('/show/', {'categories': '101'})
        assert response.status_code, 200
