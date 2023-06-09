from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from blog.models import Post


class BlogTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@email.com',
            password='testpassword'
        )
        self.post = Post.objects.create(
            title='Test title',
            author=self.user,
            body='Test body'
        )

    def test_string_representation(self):
        post = Post(title='A sample title')
        self.assertEqual(str(post), post.title)

    def test_post_content(self):
        self.assertEqual(self.post.title, 'Test title')
        self.assertEqual(f'{self.post.author}', 'testuser')
        self.assertEqual(self.post.body, 'Test body')

    def test_post_list_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test body')
        self.assertTemplateUsed(response, 'home.html')

    def test_post_detail_view(self):
        response = self.client.get('/post/1/')
        no_response = self.client.get('/post/10000/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'Test title')
        self.assertTemplateUsed(response, 'post_detail.html')

    def test_post_create_view(self):
        response = self.client.post(reverse('post_new'), {
            'title': 'New title',
            'body': 'New text',
            'author': self.user,
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'New title')
        self.assertContains(response, 'New text')

    def test_post_update_view(self):
        response = self.client.post(reverse('post_edit', args='1'), {
            'title': 'edited title',
            'body': 'edited title'
        })
        self.assertEqual(response.status_code, 302)

    def test_post_delete_view(self):  # new
        response = self.client.get(reverse('post_delete', args='1'))
        self.assertEqual(response.status_code, 200)