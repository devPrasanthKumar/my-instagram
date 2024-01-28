from django.db import models

from django import forms
from instagramApp.models import UserFollowerModel, UserProfileModel, UserPostModel, CommentModel, LikeModel

from instagramAuth.models import CustomUser


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfileModel
        fields = "__all__"
        exclude = ["username", "uuid"]


class UserProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = UserProfileModel
        fields = "__all__"
        exclude = ["username", "uuid"]


class UserPostForm(forms.ModelForm):
    class Meta:
        model = UserPostModel
        fields = "__all__"
        exclude = ["username", "slug"]


class PostCommentForm(forms.ModelForm):
    class Meta:
        model = CommentModel
        fields = "__all__"


class PostLikeForm(forms.ModelForm):
    class Meta:
        model = LikeModel
        fields = []


class UserFollowForm(forms.ModelForm):
    class Meta:
        model = UserFollowerModel
        fields = []
        exclude = ["username"]
