import shutil
import tempfile

from django import forms
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from django.core.cache import cache

from posts.models import Group, Post, Follow, Comment

User = get_user_model()
TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostPagesTests(TestCase):
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
        image = SimpleUploadedFile(
            'post_image.jpg',
            content=(
                b'\x47\x49\x46\x38\x39\x61\x02\x00'
                b'\x01\x00\x80\x00\x00\x00\x00\x00'
                b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
                b'\x00\x00\x00\x2C\x00\x00\x00\x00'
                b'\x02\x00\x01\x00\x00\x02\x02\x0C'
                b'\x0A\x00\x3B'
            ),
            content_type='image/jpg')
        cls.post = Post.objects.create(
            text='Текст',
            group=cls.group,
            author=cls.author,
            image=image,
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        cache.clear()
        self.client = Client()
        self.user = User.objects.create_user(username='user')
        self.client.force_login(self.user)
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.author)

    def test_pages_uses_correct_template(self):
        templates_pages_names = {
            'posts/index.html': reverse('posts:index'),
            'posts/group_list.html': reverse('posts:group_list',
                                             kwargs={'slug': 'group-slug'}),
            'posts/post_detail.html': reverse(
                'posts:post_detail', kwargs={'post_id': self.post.id}),
            'posts/create_post.html': reverse('posts:create_post'),
            'posts/profile.html': reverse('posts:profile', args={self.author}),
        }
        for template, reverse_name in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_post_edit_page_show_correct_template(self):
        response = self.authorized_client.get(reverse(
            'posts:post_edit', kwargs={'post_id': self.post.id}))
        self.assertTemplateUsed(response, 'posts/create_post.html')

    def check_context(self, context):
        self.assertIn('page_obj', context)
        post = context['page_obj'][0]
        self.assertEqual(post.author, PostPagesTests.author)
        self.assertEqual(post.group.title, PostPagesTests.group.title)
        self.assertEqual(post.text, PostPagesTests.post.text)
        self.assertEqual(post.image, PostPagesTests.post.image)

    def test_index_page_show_correct_context(self):
        response = self.authorized_client.get(reverse('posts:index'))
        self.check_context(response.context)

    def test_profile_show_correct_context(self):
        response = self.authorized_client.get(
            reverse('posts:profile', args={self.author}))
        self.check_context(response.context)

    def test_post_group_list_page_show_correct_context(self):
        response = (self.authorized_client.get(
            reverse('posts:group_list', kwargs={'slug': 'group-slug'})))
        self.check_context(response.context)

    def test_create_post_page_show_correct_context(self):
        response = self.authorized_client.get(reverse('posts:create_post'))
        form_fields = {
            'text': forms.CharField,
            'group': forms.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_edit_post_page_show_correct_context(self):
        response = self.authorized_client.get(reverse(
            'posts:post_edit', kwargs={'post_id': self.post.id}))
        form_fields = {
            'text': forms.CharField,
            'group': forms.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_post_detail_page_show_correct_context(self):
        response = (self.authorized_client.get(
            reverse('posts:post_detail', kwargs={'post_id': self.post.id})))
        self.assertEqual(response.context.get(
            'post').group.title, self.group.title)
        self.assertEqual(response.context.get(
            'post').author, self.author)
        self.assertEqual(response.context.get('post').text, self.post.text)
        self.assertEqual(response.context.get('post').image, self.post.image)

    def test_follow(self):
        self.response = (self.client.get(
            reverse('posts:profile_follow', args={self.author})))
        self.assertIs(
            Follow.objects.filter(user=self.user, author=self.author).exists(),
            True
        )

    def test_unfollow(self):
        self.response = (self.client.get(
            reverse('posts:profile_follow', args={self.author})))
        self.response = (self.client.get(
            reverse('posts:profile_unfollow', args={self.author})))
        self.assertIs(
            Follow.objects.filter(user=self.user, author=self.author).exists(),
            False
        )

    def test_new_post_for_follow_authorized_client(self):
        Follow.objects.create(user=self.user, author=self.author)
        response = (self.client.get(reverse('posts:follow_index')))
        self.assertIn(self.post, response.context['page_obj'])

    def test_new_post_for_follow_guest_client(self):
        User.objects.create_user(username='user_test', password='pass')
        self.client.login(username='user_test', password='pass')
        response = (self.client.get(reverse('posts:follow_index')))
        self.assertNotIn(self.post, response.context['page_obj'])

    def test_comment_post_auth_user(self):
        comment = Comment.objects.create(
            text='Коментарий', author=self.user, post_id=self.post.id)
        response = (self.client.post(
            reverse('posts:add_comment', kwargs={'post_id': self.post.id})))
        response = (self.client.get(
            reverse('posts:post_detail', kwargs={'post_id': self.post.id})))
        self.assertContains(response, comment)

    def test_comment_post_guest_user(self):
        response = (self.guest_client.post(
            reverse('posts:add_comment', kwargs={'post_id': self.post.id})))
        self.assertRedirects(response, reverse(
            'users:login') + '?next=' + reverse(
                'posts:add_comment',
            kwargs={'post_id': self.post.id}))

    def test_cache(self):
        response_before = self.authorized_client.get(reverse('posts:index'))
        Post.objects.create(text='Тестовый текст', author=self.author)
        response_after = self.authorized_client.get(reverse('posts:index'))
        self.assertEqual(response_before.content, response_after.content)
        cache.clear()
        response = self.authorized_client.get(reverse('posts:index'))
        self.assertNotEqual(response_before.content, response.content)


class PaginatorViewsTest(TestCase):
    @ classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create_user(
            username='HasNoName'
        )
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='group-slug',
            description='Тестовое описание',
        )
        number_of_posts = 13
        for post in range(number_of_posts):
            Post.objects.create(text='Текст', author=cls.author,
                                group=cls.group)

    def setUp(self):
        cache.clear()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.author)

    def test_index_first_page_contains_ten_records(self):
        response = self.authorized_client.get(reverse('posts:index'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['page_obj']), 10)

    def test_index_second_page_contains_three_records(self):
        response = self.authorized_client.get(
            reverse('posts:index') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['page_obj']), 3)

    def test_group_list_first_page_contains_ten_records(self):
        response = self.authorized_client.get(
            reverse('posts:group_list', kwargs={'slug': 'group-slug'}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['page_obj']), 10)

    def test_group_list_second_page_contains_three_records(self):
        response = self.authorized_client.get(reverse(
            'posts:group_list',
            kwargs={'slug': 'group-slug'}) + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['page_obj']), 3)

    def test_profile_first_page_contains(self):
        response = self.authorized_client.get(
            reverse('posts:profile', args={self.author}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['page_obj']), 10)

    def test_profile_second_page_contains(self):
        response = self.authorized_client.get(
            reverse('posts:profile', args={self.author}) + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['page_obj']), 3)
