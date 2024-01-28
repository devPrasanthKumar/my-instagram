from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View

# Create your views here.
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from instagramApp.forms import PostLikeForm, UserPostForm, UserProfileForm, PostCommentForm, UserProfileUpdateForm
from instagramApp.models import CommentModel, LikeModel, UserFollowerModel, UserPostModel, UserProfileModel
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from instagramAuth.models import CustomUser

import uuid
# home view


class CreateProfileView(LoginRequiredMixin, CreateView):
    login_url = "login"
    model = UserProfileModel
    form_class = UserProfileForm
    template_name = "user_auth/user_profile.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.instance.username = self.request.user
        form.instance.uuid = uuid.uuid4()
        form.save()
        print("print saved")
        return super().form_valid(form)


class UpdateProfileView(UpdateView):
    model = UserProfileModel
    form_class = UserProfileUpdateForm
    success_url = reverse_lazy("home")
    template_name = "user_auth/update_profile.html"
    pk_url_kwarg = "uuid"

    def get_object(self, **kwargs):
        token = self.kwargs.get("uuid")
        print(token)
        user = get_object_or_404(UserProfileModel, uuid=token)
        return user

    # """
    # it helps to override the form's data , which is the data displayed when you visit the update form.
    # """

    # def get_initial(self):

    #     # get user profile's data by "username ",its related to the Custom User
    #     user_profile = get_object_or_404(
    #         UserProfileModel, username=self.request.user)

    #     return {'username': user_profile.username}


class CreatePostView(LoginRequiredMixin, FormView):
    login_url = "login"
    form_class = UserPostForm
    template_name = "main/add_post.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        user_profile, created = UserProfileModel.objects.get_or_create(
            username=self.request.user)
        form.instance.username = user_profile
        form.save()
        return super().form_valid(form)


class UpdatePostView(LoginRequiredMixin, UpdateView):
    login_url = "login"
    template_name = "main/update_post.html"
    form_class = UserPostForm
    model = UserPostModel
    success_url = reverse_lazy("home")


class DeletePostView(LoginRequiredMixin, DeleteView):
    login_url = "login"
    model = UserPostModel
    template_name = "main/delete_post.html"
    success_url = reverse_lazy("home")
    context_object_name = "delete"


class ShowPostAndCommentView(LoginRequiredMixin, ListView):
    login_url = "login"
    template_name = "main/home.html"
    context_object_name = "posts"
    model = UserPostModel


class CreateCommentView(LoginRequiredMixin, View):
    login_url = "login"

    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            getComment = request.POST.get("postComment")
            print("my comment ************** ", getComment)
            getPostID = self.kwargs.get("pk")
            get_post = get_object_or_404(UserPostModel, pk=getPostID)
            getUserID = self.request.user
            CommentModel.objects.create(
                comment=getComment, comment_post=get_post, comment_username=getUserID)
            return redirect("home")

        return render(request, "main/home.html")


class LikeView(LoginRequiredMixin, FormView):
    login_url = "login"
    form_class = PostLikeForm
    template_name = "main/home.html"
    success_url = reverse_lazy("home")
    model = LikeModel

    def form_valid(self, form):

        getID = self.kwargs.get("pk")
        post_data = get_object_or_404(UserPostModel, pk=getID)
        form.instance.like_post = post_data
        form.instance.like_username = self.request.user
        try:
            exist_like = LikeModel.objects.get(
                Q(like_username=self.request.user) & Q(like_post=post_data)
            )
            exist_like.delete()

        except LikeModel.DoesNotExist:
            LikeModel.objects.create(
                like_username=self.request.user, like_post=post_data)

        return super().form_valid(form)


class UserFollowerView(LoginRequiredMixin, CreateView):
    model = UserFollowerModel
    login_url = "login"
    fields = []
    template_name = "user_auth/show_all_user.html"
    success_url = reverse_lazy("home")
    pk_url_kwarg = "uuid"

    def form_valid(self, form):

        getID = self.kwargs.get("uuid")
        post_user_data = get_object_or_404(UserProfileModel, pk=getID)
        print("post user name", post_user_data)
        current_profile_user = get_object_or_404(
            UserProfileModel, pk=self.request.user.userprofilemodel.pk)
        print(" im current  user ", current_profile_user)
        print(post_user_data)

        try:
            exist_follower = UserFollowerModel.objects.get(
                followers=post_user_data, username=current_profile_user)
            exist_follower.delete()
            print("already  folower worked")
        except:
            print("excepyt worked")
            form.instance.username = current_profile_user
            form.instance.followers = post_user_data
            form.instance.following = current_profile_user
            form.save()
            print("follow form worked")
            return super().form_valid(form)

        return super().form_valid(form)
