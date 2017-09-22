from django.db import models
from django.contrib.auth.models import User
from address.models import State, City


def post_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'post_images/{0}/{1}'.format(instance.user.username, filename)


class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# Post Module
class Post(TimeStampedModel):
    # basic
    post_title = models.CharField(
        max_length=200,
        null=False
    )

    post_description = models.TextField(max_length=160)

    # picture
    post_picture = models.FileField(
        null=False,
        blank=False,
        upload_to=post_directory_path
    )

    # The location of the picture
    post_state = models.ForeignKey(
        State,
        related_name='state'
    )

    post_city = models.ForeignKey(
        City,
        related_name='city'
    )

    # user who creates the post
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    likes = models.ManyToManyField(User, related_name='likes_posts', blank=True)

    show = models.BooleanField(default=True)

    numberOfLikes = models.PositiveIntegerField(default=0)

    file_type = models.CharField(max_length=10, null=True)

    numberOfComment = models.PositiveIntegerField(default = 0)

    def __str__(self):
        return self.post_title

class Comment(TimeStampedModel):
    content = models.CharField(max_length=160, null=False, default=None)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    belong_post = models.ForeignKey(Post, on_delete=models.CASCADE, default=None)