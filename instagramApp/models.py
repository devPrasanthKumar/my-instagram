from typing import Any
from django.db import models

from instagramAuth.models import CustomUser
from django.utils.text import slugify
# Create your models here.

# user profile
import uuid


class UserProfileModel(models.Model):

    GENDER = [
        ("Male", "Male"), ("Female", "Female"), ("Others", "Others")
    ]

    username = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE)
    user = models.CharField(max_length=3000)
    uuid = models.CharField(
        unique=True, default=uuid.uuid4(), max_length=36, primary_key=True)
    profile_img = models.ImageField(
        upload_to="user_profile/", default="uploads/boys.jpg")
    bio = models.TextField(max_length=1000)
    website = models.URLField(max_length=1000, null=True, blank=True)
    gender = models.CharField(choices=GENDER, max_length=30)

    def __str__(self):
        return str(self.username.username)


class UserFollowerModel(models.Model):
    username = models.ForeignKey(UserProfileModel, on_delete=models.CASCADE)
    followers = models.ForeignKey(
        UserProfileModel, on_delete=models.CASCADE, related_name="followers", null=True, blank=True)
    following = models.ForeignKey(
        UserProfileModel, on_delete=models.CASCADE, related_name="followinig", null=True, blank=True)

    def __str__(self):
        return str(self.followers)


class UserPostModel(models.Model):
    username = models.ForeignKey(
        UserProfileModel, on_delete=models.CASCADE, related_name="userpostmodel")
    title = models.CharField(max_length=500)
    caption = models.TextField()
    slug = models.SlugField(unique=True, blank=True, null=True)
    image = models.ImageField(upload_to="uploads/")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def delete(self):
        self.image.delete()
        return super().delete()


class CommentModel(models.Model):
    comment = models.CharField(max_length=1000)
    comment_post = models.ForeignKey(
        UserPostModel, on_delete=models.CASCADE, related_name="subcomment")
    comment_username = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="commentuser")


class LikeModel(models.Model):
    like_post = models.ForeignKey(
        UserPostModel, on_delete=models.CASCADE, related_name="likeforpost")
    like_username = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.like_username} liked for {self.like_post}'
