from django.db import migrations, models

from django.contrib.auth.models import User
from .middleware import get_current_user
from django.db.models import Q


class Category(models.Model):  # модель "Категории" для "Объявления"
    category_name = models.CharField(max_length=20,
                                     verbose_name="Категория персонажа",
                                     )
    subscribers = models.ManyToManyField(User, blank=True, related_name='categories')

    def __str__(self):
        return self.category_name


class Post(models.Model):  # модель "Объявления"
    title = models.CharField(max_length=128,
                             unique=True,
                             error_messages='Новость с таким заголовком уже есть',
                             blank=False,
                             )
    text = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post_category = models.ManyToManyField(Category, through='PostCategory')
    content = models.FileField(upload_to='media/', blank=True)

    def __str__(self):
        return f'{self.title}: {self.text}'

    def preview(self):
        return self.text[0:123] + '...'

    def get_absolute_url(self):
        return f'/post/{self.id}'

    def get_thumbnail(self):
        if not self.content:
            return '/media/media/default.jpg'
        return self.content.url


class PostCategory(models.Model):
    post_through = models.ForeignKey(Post, on_delete=models.CASCADE)
    category_through = models.ForeignKey(Category, on_delete=models.CASCADE)


class StatusRelpy(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(Q(status=False, reply_user=get_current_user())
                                             | Q(status=False, reply_post__author=get_current_user())
                                             | Q(status=True))


class Reply(models.Model):  # модель "Отклик"
    reply_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор комментария', blank=True, null=True)  # связь с Пользователем
    reply_post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Статья', blank=True, null=True, related_name='relpy_post')  # связь с Объявлением
    text = models.TextField(verbose_name='Текст комментария')  # в Отклике может быть только текст
    reply_date_creation = models.DateTimeField(auto_now=True)
    status = models.BooleanField(verbose_name='status_reply', default=False)
    objects = StatusRelpy()

    def __str__(self):
        return f'{self.text[:10]}'


