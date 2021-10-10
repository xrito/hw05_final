from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.core.cache import cache
from django.urls import reverse

from posts.models import Post, Group

User = get_user_model()


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create_user(
            username='HasNoName',
        )
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='group-slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=cls.author,
            group=cls.group,
        )

    def setUp(self):
        cache.clear()
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.author)

    def test_urls_uses_correct_template(self):
        templates_url_names = {
            'posts/index.html': '/',
            'posts/profile.html': '/profile/HasNoName/',
            'posts/group_list.html': '/group/group-slug/',
            'posts/post_detail.html': reverse(
                'posts:post_detail', kwargs={'post_id': self.post.id}),
        }
        for template, adress in templates_url_names.items():
            with self.subTest(adress=adress):
                response = self.guest_client.get(adress)
                self.assertTemplateUsed(response, template)

    def test_post_list_url_authorized_client_create(self):
        response = self.authorized_client.get('/create/')
        self.assertEqual(response.status_code, 200)

    def test_post_list_url_authorized_client_edit(self):
        response = self.authorized_client.get(
            reverse('posts:post_detail', kwargs={'post_id': self.post.id}))
        self.assertEqual(response.status_code, 200)

    def test_post_url_non_existent_page(self):
        response = self.guest_client.get('unexistent_page/')
        self.assertEqual(response.status_code, 404)
