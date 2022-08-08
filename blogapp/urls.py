from django.urls import path
from blogapp import views
urlpatterns=[
    path("accounts/signup",views.SignUpView.as_view(),name="signup"),
    path("accounts/signin",views.LoginView.as_view(),name="signin"),
    path("accounts/signout", views.signout, name="signout"),
    path("home",views.IndexView.as_view(),name="home"),
    path("users/profile/add",views.CreateUserProfileView.as_view(),name="add-profile"),
    path("users/password/change", views.PasswordResetView.as_view(), name="password-reset"),
    path("users/profile/change/<int:user_id>", views.UpdateProfileView.as_view(), name="profile-update"),
    path("post/comment/<int:post_id>",views.add_comment,name="add-comment"),
    path("post/like/add/<int:post_id>",views.add_like,name="add-like"),
    path("post/like/remove/<int:post_id>",views.dislike,name="dislike"),
    path("post/comment/remove/<int:post_id>/<int:comment_id>",views.delete_comment,name="delete-comment"),
    path("users/profile/profile/pic_update/<int:user_id>",views.ProfilePicUpdateView.as_view(),name="pro-pic-update"),
    path("users/follow/<int:user_id>",views.follow,name="follow"),
    path("users/unfollow/<int:user_id>",views.unfollow,name="unfollow"),
    path("post/remove/<int:post_id>",views.delete_post,name="delete-post"),
    path("post/update/<int:post_id>",views.UpdateBlogView.as_view(),name="update-post"),
    path("post/comment/update/<int:comment_id>", views.UpdateCommentView.as_view(), name="update-comment"),
    path("accounts/remove/<int:user_id>", views.DeleteProfileView.as_view(), name="delete-profile"),
    path("post/comment/like/<int:cmt_id>",views.like_comment,name="like-comment"),
    path("post/comment/unlike/<int:cmt_id>",views.unlike_comment,name="unlike-comment"),
    path("users/profile/profile/coverpic_update/<int:user_id>",views.CoverPicUpdateView.as_view(),name="coverpic-update"),
    path("users/profile/view",views.ViewMyProfileView.as_view(),name="view-myprofile"),






]