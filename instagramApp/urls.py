from django.urls import path
from . import views


urlpatterns = [
    path("home/", views.ShowPostAndCommentView.as_view(), name="home"),
    path("createprofile/", views.CreateProfileView.as_view(), name="createprofile"),
    path("updateprofile/<uuid:uuid>",
         views.UpdateProfileView.as_view(), name="update-profile"),
    path("createpost/", views.CreatePostView.as_view(), name="createpost"),
    path("follow/<uuid:uuid>", views.UserFollowerView.as_view(), name="follow"),

    path("update-post/<int:pk>", views.UpdatePostView.as_view(), name="update-post"),
    path("delete-post/<int:pk>", views.DeletePostView.as_view(), name="delete-post"),

    path("comment/<int:pk>", views.CreateCommentView.as_view(), name="comment"),
    path("like/<int:pk>", views.LikeView.as_view(), name="like"),


]
