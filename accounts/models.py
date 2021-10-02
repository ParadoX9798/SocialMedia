from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.PositiveSmallIntegerField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    phone = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.user.username}'


def save_profile(sender, **kwargs):
    if kwargs["created"]:
        p1 = Profile(user=kwargs['instance'])
        p1.save()


post_save.connect(receiver=save_profile, sender=User)


class Relations(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return f'{self.from_user} following {self.to_user}'
