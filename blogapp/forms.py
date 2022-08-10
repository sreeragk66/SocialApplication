from django.contrib.auth.models import User
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from blogapp.models import UserProfile,Blogs,Comments
class UserRegistrationForm(UserCreationForm):
    class Meta:
        model=User
        fields=[
            "first_name",
            "last_name",
            "email",
            "username",
            "password1",
            "password2"
        ]

class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput())



class UserProfileForm(ModelForm):
    class Meta:
        model=UserProfile
        exclude=("user","following","saved_posts")
        widgets={
            "date_of_birth":forms.DateInput(attrs={"class":"form-control","type":"date"}),
            "bio":forms.TextInput(attrs={"class":"form-control"}),
            "phone":forms.TextInput(attrs={"class":"form-control"}),
            "profile_pic": forms.FileInput(attrs={"class": "form-control"}),
            "cover_pic": forms.FileInput(attrs={"class": "form-control"}),
            "gender":forms.Select(attrs={"class":"form-control"}),

        }

class PasswordResetForm(forms.Form):
    old_password=forms.CharField(widget=forms.PasswordInput)
    new_password=forms.CharField(widget=forms.PasswordInput)
    confirm_password=forms.CharField(widget=forms.PasswordInput)


class BlogForm(ModelForm):
    class Meta:
        model=Blogs
        fields=[
            "title","description","image"
        ]
        widgets={
            "title":forms.TextInput(attrs={"class":"form-control"}),
            "description":forms.Textarea(attrs={"class":"form-control"}),
            "image":forms.FileInput(attrs={"class":"form-control"}),
        }

class CommentForm(ModelForm):
    class Meta:
        model=Comments
        fields=[
            "comment"
        ]
        widgets={
            "comment":forms.TextInput(attrs={"class":"form-control"})
        }

class ProfilePicUpdateForm(ModelForm):
    class Meta:
        model=UserProfile
        fields=[
            "profile_pic"
        ]
        widgets={
            "profile_pic":forms.FileInput(attrs={"class":"form-control"})
    }

class DeleteProfileForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control","placeholder":"Enter password to confirm"}))


class CoverPicUpdateForm(ModelForm):
    class Meta:
        model=UserProfile
        fields=[
            "cover_pic"
        ]
        widgets={
            "cover_pic":forms.FileInput(attrs={"class":"form-control"})
    }