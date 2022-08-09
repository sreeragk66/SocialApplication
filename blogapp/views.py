from django.shortcuts import render,redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import View,CreateView,FormView,TemplateView,UpdateView,DeleteView
from django.contrib.auth.models import User
from blogapp.models import UserProfile,Blogs,Comments
from blogapp.forms import UserRegistrationForm,LoginForm,UserProfileForm,PasswordResetForm,BlogForm,CommentForm,ProfilePicUpdateForm,DeleteProfileForm,CoverPicUpdateForm
from django.contrib.auth import login,logout,authenticate
from django.utils.decorators import method_decorator


# Create your views here.

def signin_required(func):
    def wrapper(request,*args,**kwargs):
        if request.user.is_authenticated:

            return func(request,*args,**kwargs)
        else:
            messages.error(request, "Access denied  you must login !")
            return redirect("signin")
    return wrapper

class SignUpView(CreateView):
    form_class=UserRegistrationForm
    template_name="user-registration.html"
    model=User

    def post(self,request,*args,**kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'User has been added successfully.')
            return redirect("signin")
        else:
            messages.error(request,"Failed to create user, Please check the entered data")
            return render(request,self.template_name,{"form":form})


class LoginView(FormView):
    model=User
    template_name="user-login.html"
    form_class=LoginForm

    def post(self,request,*args,**kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get("username")
            password=form.cleaned_data.get("password")
            user=authenticate(request,username=username,password=password)

            if user:
                login(request,user)
                messages.success(request,f"Welcome {request.user}")
                return redirect("home")
            else:
                messages.error(request, "Incorrect username or password")
                return render(request,self.template_name,{"form":form})

# To display blog posts,likes and comments
@method_decorator(signin_required,name="dispatch")
class IndexView(CreateView):
    template_name="home.html"
    form_class=BlogForm
    success_url = reverse_lazy("home")
    template_name="home.html"

    def form_valid(self, form):
        form.instance.author=self.request.user
        messages.success(self.request,"Post has been saved")
        self.object=form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        comment_form=CommentForm()
        blogs = Blogs.objects.all().order_by("-posted_date")
        # check if a user has userprofile
        if hasattr(self.request.user,'users'):
            followings=self.request.user.users.fetch_followings
            filtered_blogs=[blog for blog in blogs if blog.author in followings]
            context["blogs"]=filtered_blogs
            context["comment_form"] = comment_form
            return context
        else:
            context["comment_form"]=comment_form
            return context



@method_decorator(signin_required,name="dispatch")
class CreateUserProfileView(CreateView):
    model=UserProfile
    template_name = "add-profile.html"
    form_class=UserProfileForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.instance.user=self.request.user
        messages.success(self.request,"Profile has been added")
        self.object=form.save()
        return super().form_valid(form)


@method_decorator(signin_required,name="dispatch")
class PasswordResetView(FormView):
    template_name = "password-reset.html"
    form_class=PasswordResetForm

    def post(self,request,*args,**kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            old_password=form.cleaned_data.get("old_password")
            password1=form.cleaned_data.get("new_password")
            password2=form.cleaned_data.get("confirm_password")
            if password1==password2:
                user=authenticate(request,username=request.user.username,password=old_password)
                if user:
                    user.set_password(password2)
                    user.save()
                    messages.success(request,"Password has been changed, Please login to continue")
                    return redirect("signin")

                else:
                    messages.error(request,"invalid credentials !")
                    return render(request,self.template_name,{"form":form})
            else:
                messages.error(request, "Passwords do not match ! Please recheck")
                return render(request, self.template_name, {"form": form})

@method_decorator(signin_required,name="dispatch")
class UpdateProfileView(UpdateView):
    model=UserProfile
    form_class=UserProfileForm
    template_name = "profile-update.html"
    success_url = reverse_lazy("home")
    pk_url_kwarg = "user_id"

    def form_valid(self, form):
        messages.success(self.request,"Profile has been updated")
        self.object=form.save()
        return super().form_valid(form)

@signin_required
def add_comment(request,*args,**kwargs):
    if request.method=="POST":
        blog_id=kwargs.get('post_id')
        blog=Blogs.objects.get(id=blog_id)
        user=request.user
        comment=request.POST.get("comment")
        Comments.objects.create(blog=blog,comment=comment,user=user)
        messages.success(request,"Comment has been added")
        return redirect("home")

@signin_required
def delete_comment(request,*args,**kwargs):
    blog_id = kwargs.get('post_id')
    comment_data=kwargs.get('comment_id')
    blog=Blogs.objects.get(id=blog_id)
    all_comments=blog.comments_set.all()
    for comment in all_comments:
        if comment.user == request.user and comment.id ==comment_data:
            comment.delete()
            messages.error(request,"Comment deleted")
    return redirect("home")



@signin_required
def add_like(request,*args,**kwargs):
    blog_id=kwargs.get("post_id")
    blog=Blogs.objects.get(id=blog_id)
    blog.Liked_by.add(request.user)
    blog.save()
    return redirect("home")


@signin_required
def dislike(request,*args,**kwargs):
    blog_id = kwargs.get("post_id")
    blog = Blogs.objects.get(id=blog_id)
    blog.Liked_by.remove(request.user)
    return redirect("home")

@method_decorator(signin_required,name="dispatch")
class ProfilePicUpdateView(UpdateView):
    model=UserProfile
    form_class=ProfilePicUpdateForm
    template_name = "profile-pic-update.html"
    success_url = reverse_lazy("home")
    pk_url_kwarg = "user_id"

    def form_valid(self, form):
        messages.success(self.request,"Profile Picture has been updated")
        self.object=form.save()
        return super().form_valid(form)


@signin_required
def signout(request,*args,**kwargs):
    logout(request)
    messages.error(request,"Logged out")
    return redirect("signin")

@signin_required
def delete_post(request,*args,**kwargs):
    blog_id=kwargs.get("post_id")
    blog=Blogs.objects.get(id=blog_id)
    if blog.author==request.user:
        blog.delete()
        messages.error(request,"Post has been deleted")
        return redirect("home")
    else:
        messages.error(request,"Cannot delete post !")
        return redirect("home")

@signin_required
def follow(request,*args,**kwargs):
    friend_id=kwargs.get("user_id")
    if friend_id == request.user.id:
        messages.error(request,"You can only follow other users")
        return redirect("home")
    else:
        friend_profile=User.objects.get(id=friend_id)
        request.user.users.following.add(friend_profile)
        friend_profile.save()
        messages.success(request,"You have followed  "+friend_profile.username)
        return redirect("home")

@signin_required
def unfollow(request,*args,**kwargs):
    friend_id=kwargs.get("user_id")
    friend_profile=User.objects.get(id=friend_id)
    request.user.users.following.remove(friend_profile)
    friend_profile.save()
    messages.success(request,"You have unfollowed  "+friend_profile.username)
    return redirect("home")

@method_decorator(signin_required,name="dispatch")
class UpdateBlogView(UpdateView):
    model=Blogs
    form_class=BlogForm
    template_name="edit-post.html"
    success_url = reverse_lazy("home")
    pk_url_kwarg ="post_id"

    def form_valid(self, form):
        messages.success(self.request,"Post has been Updated")
        self.object=form.save()
        return super().form_valid(form)

@method_decorator(signin_required,name="dispatch")
class UpdateCommentView(UpdateView):
    model=Comments
    form_class=CommentForm
    template_name="edit-comment.html"
    success_url = reverse_lazy("home")
    pk_url_kwarg = "comment_id"


    def form_valid(self, form):
        messages.success(self.request,"Comment Updated")
        self.object=form.save()
        return super().form_valid(form)


@method_decorator(signin_required,name="dispatch")
class DeleteProfileView(DeleteView):
    model=User
    form_class=DeleteProfileForm
    template_name = "delete-account.html"
    success_url = reverse_lazy("signup")
    pk_url_kwarg = "user_id"

    def post(self,request,*args,**kwargs):
        form=self.form_class(request.POST)
        qs = User.objects.get(id=request.user.id)
        user_id=kwargs.get("user_id")
        if user_id == request.user.id:
            if form.is_valid():
                password=form.cleaned_data.get("password")
                user=authenticate(username=request.user,password=password)
                if user:
                    qs.delete()
                    messages.error(self.request, "Your account has been deleted ! Please signup")
                    return redirect("signup")
                else:
                    messages.error(self.request, "Password is Incorrect !")
                    return render(request,self.template_name,{"form":form})
        else:
            messages.error(request,"Access denied, Cannot delete other users' account")
            return render(request,self.template_name,{"form":form})



@signin_required
def like_comment(request,*args,**kwargs):
    cmt_id=kwargs.get("cmt_id")
    comment=Comments.objects.get(id=cmt_id)
    comment.liked_by.add(request.user)
    comment.save()
    return redirect("home")

@signin_required
def unlike_comment(request,*args,**kwargs):
    cmt_id=kwargs.get("cmt_id")
    comment=Comments.objects.get(id=cmt_id)
    comment.liked_by.remove(request.user)
    return redirect("home")


@method_decorator(signin_required,name="dispatch")
class CoverPicUpdateView(UpdateView):
    model=UserProfile
    form_class=CoverPicUpdateForm
    template_name = "cover-pic-update.html"
    success_url = reverse_lazy("home")
    pk_url_kwarg = "user_id"

    def form_valid(self, form):
        messages.success(self.request,"Cover Picture has been updated")
        self.object=form.save()
        return super().form_valid(form)




@method_decorator(signin_required,name="dispatch")
class ViewMyProfileView(CreateView):
    template_name="my-profile.html"
    form_class=BlogForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.instance.author=self.request.user
        messages.success(self.request,"Post has been saved")
        self.object=form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        comment_form=CommentForm()
        #exclude posts by loggedin user
        blogs=Blogs.objects.filter(author=self.request.user)
        context["blogs"]=blogs.order_by("-posted_date")
        context["comment_form"]=comment_form
        return context

class ViewOthersProfile(TemplateView):
    template_name = "others-profile.html"

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        user_id = kwargs.get("user_id")
        user=User.objects.get(id=user_id)
        blogs=Blogs.objects.filter(author=user.id)
        context["user"]=user
        context["blogs"]=blogs.order_by("-posted_date")
        return context
