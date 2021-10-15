from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Post(models.Model):
    text = models.TextField(
        verbose_name='Текст поста', help_text='Текст нового поста'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата публикации', db_index=True)
    group = models.ForeignKey(
        'Group',
        on_delete=models.SET_NULL,
        blank=True, null=True,
        max_length=255,
        related_name='posts',
        verbose_name='Группа',
        help_text='Группа, к которой будет относиться пост'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор'
    )
    image = models.ImageField(
        'Картинка',
        upload_to='posts/',
        blank=True,
        null=True,
        help_text='Загрузите картинку'
    )
    post_views = models.IntegerField(default=0)

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.text


class Group(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    description = models.TextField(max_length=400)

    def __str__(self):
        return str(self.title)


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Коментарий к'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор коментария'
    )
    text = models.TextField(
        verbose_name='Текст коментария', help_text='Текст нового коментария'
    )
    created = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата публикации коментария')

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.text


class Follow(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='follower')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='following')
