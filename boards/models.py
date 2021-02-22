from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from toy_board_with_django.settings import AUTH_USER_MODEL


class TimeStampedModel(models.Model):
    created_datetime = models.DateTimeField(auto_now_add=True, blank=True)
    updated_datetime = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        abstract = True
        ordering = ('-created_datetime',)


class Post(TimeStampedModel):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='posts', null=True, blank=True)
    title = models.CharField(_('제목'), max_length=50)
    content = models.TextField(_('내용'))
    content_text = models.TextField(_('평문 내용'), null=True, blank=True)
    views = models.PositiveIntegerField(_('조회수'), default=0, blank=True)
    password = models.CharField(_('비밀번호'), max_length=100, null=True, blank=True)

    class Meta:
        ordering = ('-created_datetime', )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("boards:post_detail", args=(self.id,))


class Favorite(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorites')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='favorites')


class Comment(TimeStampedModel):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='comments', null=True, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(_('내용'))
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    root = models.ForeignKey('self', null=True, blank=True, related_name='comments', on_delete=models.CASCADE)
    is_delete = models.BooleanField(default=False)
    password = models.CharField(_('비밀번호'), max_length=100, null=True, blank=True)

    class Meta:
        ordering = ('-created_datetime', )

    def __str__(self):
        return f"{self.post.title} > {self.content}"

    def get_absolute_url(self):
        return reverse("boards:post_detail", args=(self.id, ))


class UploadFile(TimeStampedModel):

    def get_file_path(self, filename):
        return f"post/{timezone.now().strftime('%Y%m%D')}/{filename}"

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='upload_files', null=True, blank=True)
    file = models.FileField(_('파일'), upload_to=get_file_path)
