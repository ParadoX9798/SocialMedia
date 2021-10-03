from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField(max_length=500)
    slug = models.SlugField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.body[:30]}'

    def get_absolute_url(self):
        return reverse("post:post_detail", args=[self.created.year, self.created.month, self.created.day, self.slug])

    def count_like(self):
        return self.plike.count()

    def user_can_like(self, user):
        user_like = user.ulike.all()
        qs = user_like.filter(post_list=self)
        if qs.exists():
            return True
        return False

    def likes(self):
        post_likes = self.plike.all()
        qs = post_likes.values_list("user_like_id", flat=True)
        return qs


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ucomment')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='pcomment')
    reply = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='rcomment')
    is_reply = models.BooleanField(default=False)
    body = models.TextField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.body[:30]}'

    class Meta:
        ordering = ("created",)


class Like(models.Model):
    user_like = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ulike')
    post_list = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='plike')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user_like} liked {self.post_list.body[:10]}'
