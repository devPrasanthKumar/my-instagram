from django.contrib import admin
from .models import UserFollowerModel, UserPostModel, UserProfileModel, CommentModel, LikeModel
# Register your models here.


admin.site.register(UserProfileModel)
admin.site.register(CommentModel)


class LikeAdmin(admin.ModelAdmin):
    list_display = ["id", "like_post", "like_username"]


class PostAdmin(admin.ModelAdmin):
    list_display = ["id"]


class FollowAdmin(admin.ModelAdmin):
    list_display = ["id"]


class FollowingAdmin(admin.ModelAdmin):
    list_display = ["id", "followers", "follwing"]


admin.site.register(UserPostModel, PostAdmin)

admin.site.register(LikeModel, LikeAdmin)

admin.site.register(UserFollowerModel, FollowAdmin)
