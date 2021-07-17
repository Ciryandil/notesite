from django.contrib.auth import login
from django.core.exceptions import ValidationError
from django.http.response import FileResponse, Http404
from django.shortcuts import render, get_object_or_404
from .models import Post, Comment, UserProfile, Vote
from django.utils import timezone
from django.shortcuts import redirect
from .forms import PostForm, UserProfileForm, UserRegistrationForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from taggit.models import Tag
from django.db.models import Q
from django.views.generic import ListView
from django.core.exceptions import PermissionDenied

import datetime
import dropbox
import os
# Create your views here.


# *********************************POST RELATED VIEWS**********************************************************************
def post_list(request):
    
    
        posts = Post.objects.all().order_by('-created_date')
        return render(request, 'blog/post_list.html',{'object_list': posts})

def post_detail(request, slug):
   
    # get post object
    post = get_object_or_404(Post, slug=slug)
    comments = Comment.objects.filter(post=post, parent=None)
    upvote_count = post.get_votecount(type="upvote")
    downvote_count = post.get_votecount(type="downvote")
    url = get_note(slug)
    flag = 0 
    if request.user.is_authenticated and Vote.objects.filter(post=post,author=request.user).count() > 0:
        vote = Vote.objects.filter(post=post,author=request.user).first()
        if vote.score == 1:
            flag = 1
        elif vote.score == 2:
            flag = 2
    return render(request,
                  'blog/post_detail.html',{'post':post, 'comments': comments, 'upvotes': upvote_count, 
                  'downvotes': downvote_count, 'flag':flag, 'url': url,
                  })

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit = False)
            post.author = request.user
            post.created_date = timezone.now()
            post.slug = slugify(post.author.username + '/' + post.title + str(post.created_date))
            post.save()
            
            form.save_m2m()
            return redirect('post_detail', slug = post.slug)
    else:
        form = PostForm()
    return render(request,'blog/post_edit.html',{'form': form})

def post_edit(request, slug):
    
    post = get_object_or_404(Post, slug = slug)
    if post.author != request.user:
        raise PermissionDenied
    if request.method == "POST":
        form = PostForm(request.POST, instance = post)
        if form.is_valid:
            post = form.save(commit = False)
            post.author = request.user
            post.created_date = timezone.now()
            post.save()
            form.save_m2m()
            return redirect('post_detail', slug = post.slug)
    else:
        
        form = PostForm(instance = post)
    return render(request,'blog/post_edit.html',{'form': form})

def add_comment_to_post(request, slug):
    
    if request.method == "POST":
        text  = request.POST.get('comment')
        author = request.user
        post = get_object_or_404(Post,slug=slug)
        parent_id = request.POST.get('parent_id')
        if parent_id == "":
            comment = Comment(post=post, author=author, text=text)
            comment.save()
        else:
            parent = get_object_or_404(Comment,id=parent_id)
            comment = Comment(post=post,author=author,text=text,parent=parent)
            comment.save()
    
    return redirect('post_detail', slug=post.slug)
     

def post_remove(request, slug):
    
    post = get_object_or_404(Post, slug=slug)
    if post.author != request.user:
        raise PermissionDenied
    post.delete()
    return redirect('post_list')

def get_note(slug):
    post = get_object_or_404(Post, slug = slug)
    filepath = post.note.name
    dbx = dropbox.Dropbox(os.environ['DROPBOX_OAUTH2_TOKEN'])
    url = dbx.sharing_create_shared_link(path = filepath,  short_url=False, pending_upload=None)
    return url

def vote(request, slug, value):
    user = request.user
    post = get_object_or_404(Post, slug = slug)
    if not request.user.is_authenticated:
        raise PermissionDenied
        
    past_vote = Vote.objects.filter(author=user,post=post).count()
    if past_vote == 0:
        new_vote = Vote(post=post, author=user,score=value)
        new_vote.save()
    else:
        old_vote = Vote.objects.filter(author=user,post=post).first()
        if old_vote.score == value:
            old_vote.score = 0
        else:
            old_vote.score = value
        old_vote.save()
    if value == 1:
        post.upvotes += 1
        post.save()

    return redirect('post_detail',slug=slug)


# ****************************************************************************************************************************


#**********************************USER RELATED VIEWS*************************************************************************

def profile(request, username = None):
    if User.objects.get(username=username):
        user = User.objects.get(username = username)
        
        posts = Post.objects.filter(author = user).order_by('-created_date')
        date_joined = user.date_joined.date()
        last_active = user.last_login
        follows = False
        if request.user.is_authenticated and request.user.userprofile.following.filter(user=user).exists():
            follows = True
        return render(request, 'registration/dashboard.html',{'object_list': posts,'member':user, 'follows':follows})
    
    else:
        return render("User not found")

def register(request):
    
    if request.method == "POST":
        
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit = True)
            userprofile = UserProfile(user = user)
            userprofile.save()
            login(request, user)
            return redirect('profile', username = user.username)
    else:
        form = UserRegistrationForm()
    return render(request,'registration/register.html',{'form':form})

def set_picture(request, username = None):
   
   if not request.user.isauthenticated:
       raise PermissionDenied
   if request.user.username != username:
        raise PermissionDenied
   try:
    userprofile = request.user.userprofile
   except UserProfile.DoesNotExist:
       userprofile = UserProfile(user=request.user)


   if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance = userprofile)
        if form.is_valid:
            userprof = form.save(commit = False)
            userprof.user = request.user
            userprof.created_date = request.user.date_joined
            userprof.save()
            
            return redirect('profile', username = username)
   else:
        
        form = UserProfileForm(instance=userprofile)
   return render(request,'blog/profilepicture.html',{'form': form})

def set_follow(request, username = None):
    if not request.user.is_authenticated:
       raise PermissionDenied
    if User.objects.filter(username=username).exists():
        user = User.objects.get(username = username)
        profile1 = user.userprofile
        request.user.userprofile.following.add(profile1)

        return redirect('profile', username=username)
    else:
        return render("User not found")

def set_unfollow(request, username = None):
    if not request.user.is_authenticated:
       raise PermissionDenied
    if User.objects.filter(username=username).exists():
        user = User.objects.get(username=username)
        profile1 = user.userprofile
        request.user.userprofile.following.remove(profile1)

        return redirect('profile', username=username)

    else:
        return render("User not found")

def add_topic(request, slug):
    tag = get_object_or_404(Tag,slug=slug)
    if not request.user.is_authenticated:
       raise PermissionDenied 
    request.user.userprofile.tags.add(tag)

    return redirect(get_tagged,slug = slug)

def remove_topic(request, slug):
    if not request.user.is_authenticated:
       raise PermissionDenied
    tag = get_object_or_404(Tag,slug=slug)
    request.user.userprofile.tags.remove(tag)

    return redirect(get_tagged,slug = slug)

def create_feed(request,username):

    user = get_object_or_404(User, username=username)
    tags = user.userprofile.tags.all()
    following = user.userprofile.following.all()
        
    posts = Post.objects.filter(tags__in=tags)
        
    for userprof in following:
        member = userprof.user
        followed_posts  = Post.objects.filter(author = member)
        posts = posts | followed_posts
    posts = posts | Post.objects.filter(author = user)
    posts = posts.order_by('-created_date')
    return render(request, 'blog/post_list.html',{'object_list': posts})

def get_userlist(request, username, slug):

    user = get_object_or_404(User, username=username)
    userlist = None
    title = None
    if slug == "following":
        userlist = user.userprofile.following.all()
        title = "People Followed"
    else:
        userlist = user.userprofile.followers.all()
        title = "Followers"
    return render(request, 'blog/UserList.html', {'title':title, 'user_list':userlist})        


# ************************************************************************************************************************

#***********************************************TAG AND SEARCH RELATED VIEWS**********************************************

def get_tagged(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.objects.filter(tags=tag)
    follows = False
    if request.user.is_authenticated:
        
        if request.user.userprofile.tags.filter(slug=slug).exists():
            follows = True
    return render(request,'blog/tagged_posts.html',{'object_list':posts,'tag':slug, 'follows':follows})

def get_tagged_user(request, username, slug):
    tag = get_object_or_404(Tag,slug=slug)
    user = get_object_or_404(User,username=username)
    posts = Post.objects.filter(tags=tag,author=user)

    return render(request, 'registration/dashboard.html',{'object_list':posts, 'member':user})

class SearchView(ListView):
    model = Post
    template_name = 'post_list.html'

    def get_queryset(self):
        query = self.request.GET.get('query')
        tags = Tag.objects.filter(slug__icontains=query)
        queryset = Post.objects.filter(Q(title__icontains=query) | Q(tags__in=tags)).distinct()
        #follows = False 
        # if self.request.user.userprofile.tags.filter(tags=query).exists():
        #     follows = True
        object_list = queryset
        return object_list

class SearchUserView(ListView):
    model = Post
    template_name = 'dashboard.html'

    def get_queryset(self):
        query = self.request.GET.get('query')
        user  = get_object_or_404(User,username=self.kwargs['username'])
        tags = Tag.objects.filter(slug__icontains=query)
        query = Post.objects.filter(Q(author=user) & (Q(title__icontains=query) | Q(tags__in=tags))).distinct()
        # date_joined = user.date_joined.date()
        # last_active = user.last_login
        # follows = False
        # if self.request.user.userprofile.following.filter(user=user).exists():
        #     follows = True
        object_list = query
        return object_list



    