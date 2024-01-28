from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.UserRegisterView.as_view(), name="register"),
    path("", views.UserLoginView.as_view(), name="login"),
    path("logout/", views.UserLogoutView.as_view(), name="logout"),
    path("user-profile/<uuid:uuid>",
         views.UserProfileView.as_view(), name="user-profile"),

    path("showusers/",
         views.ShowAllUserProfilesView.as_view(), name="showusers"),


]
