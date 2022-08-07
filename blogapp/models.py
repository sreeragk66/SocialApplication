from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
import random

# Create your models here.


class UserProfile(models.Model):
    Phone_regex=RegexValidator(r'[0-9]{10}')
    profile_pic=models.ImageField(upload_to="profilepics",null=True)
    cover_pic=models.ImageField(upload_to="coverpics",null=True)
    bio=models.CharField(max_length=120)
    phone=models.CharField(max_length=10,validators=[Phone_regex])
    date_of_birth=models.DateField(null=True)
    options=(
        ("male","male"),
        ("female","female"),
        ("other","other")

    )
    gender=models.CharField(max_length=10,choices=options,default="male")
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="users")
    following=models.ManyToManyField(User,related_name="followings",blank=True)

    @property
    def fetch_followings(self):
        return self.following.all()
    @property
    def fetch_following_count(self):
        return self.fetch_followings.count()
    @property
    def get_invitations(self):
        all_users_profile=UserProfile.objects.all().exclude(user=self.user) #fetch all UserProfile objects excluding current user profile
        user_list=[userprofile.user for userprofile in all_users_profile] #taking user objects from user_list
        following_list=[u for u in self.fetch_followings]
        invitations=[user for user in user_list if user not in following_list] #excluding following list from all users
        return invitations
    @property
    def get_followers(self):
        all_users_profile = UserProfile.objects.all()
        my_followers=[]
        for profile in all_users_profile:
            if self.user in profile.fetch_followings:
                my_followers.append(profile)
        return my_followers

    @property
    def my_follower_count(self):
        return len(self.get_followers)




#fetch all users except current user




class Blogs(models.Model):
    title=models.CharField(max_length=120)
    description=models.CharField(max_length=250)
    image=models.ImageField(upload_to="blogimages",null=True)
    author=models.ForeignKey(User,on_delete=models.CASCADE,related_name="author")
    posted_date=models.DateTimeField(auto_now_add=True,null=True)
    Liked_by=models.ManyToManyField(User)

    @property
    def get_comment_count(self):
        comment_count=self.comments_set.all().count()
        return comment_count

    def __str__(self):
        return self.title

    #@property decorator used so that function can be called in template without function brackets
    @property
    def get_like_count(self):
        like_count=self.Liked_by.all().count()
        return like_count

    @property
    def get_liked_users(self):
        liked_users=self.Liked_by.all()
        users=[user.username for user in liked_users]
        return users


class Comments(models.Model):
    blog=models.ForeignKey(Blogs,on_delete=models.CASCADE)
    comment=models.CharField(max_length=160)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    liked_by=models.ManyToManyField(User,related_name="likes")
    commented_date=models.DateTimeField(auto_now_add=True,null=True)
    def get_comment_like_count(self):
        cmt_like_count=self.liked_by.all().count()
        return cmt_like_count





#fetching all comments on a blog
# blog.comments_set.all()