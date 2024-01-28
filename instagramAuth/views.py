from typing import Any
from django import http, views
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy

from instagramApp.models import UserPostModel, UserProfileModel, UserFollowerModel
from .forms import UserRegisterForm
from .models import CustomUser


# import cbv
from django.views.generic.edit import FormView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.contrib.auth.views import LoginView, LogoutView

from django.contrib.auth.mixins import LoginRequiredMixin

# create sign in


class UserRegisterView(FormView):
    form_class = UserRegisterForm
    template_name = "user_auth/user_register.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

# create login


class UserLoginView(LoginView):
    next_page = reverse_lazy("home")
    template_name = "user_auth/login.html"

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("home")

        return super().dispatch(request, *args, **kwargs)


class UserLogoutView(LoginRequiredMixin, LogoutView):
    login_url = "login"
    next_page = reverse_lazy("login")
    model = UserProfileModel


class UserProfileView(LoginRequiredMixin, DetailView):
    login_url = "login"
    model = UserProfileModel
    context_object_name = "showuserprofile"
    template_name = "user_auth/show_user_profile.html"
    pk_url_kwarg = "uuid"

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)

        getUserID = self.kwargs.get("uuid")
        post_data = get_object_or_404(
            UserProfileModel, uuid=self.request.user.userprofilemodel.uuid)
        context["postcount"] = UserPostModel.objects.filter(
            username=post_data).count()

        context["followercount"] = UserFollowerModel.objects.filter(
            followers__in=[post_data])
        context["followingcount"] = UserFollowerModel.objects.filter(
            following=post_data)

        print("my followers : ", context["followercount"])
        print("my following : ", context["followingcount"])

        context["specificuserpost"] = UserPostModel.objects.filter(
            username=post_data)
        return context


class ShowAllUserProfilesView(LoginRequiredMixin, ListView):
    login_url = "login"
    model = UserProfileModel
    context_object_name = "alluser"
    template_name = "user_auth/show_all_user.html"

    def get_queryset(self):
        return UserProfileModel.objects.exclude(username=self.request.user)
