from django.contrib.auth import login
from django.http.response import FileResponse, Http404
from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.utils import timezone
from django.shortcuts import redirect
from .forms import PostForm, UserRegistrationForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
# Create your views here.

def post_list(request):
    posts = Post.objects.all().order_by('-created_date')
    return render(request, 'blog/post_list.html',{'posts': posts})

def post_detail(request, slug):
   
    # get post object
    post = get_object_or_404(Post, slug=slug)
    comments = Comment.objects.filter(post=post, parent=None)
    
    path = '/media/' + post.note.name
    return render(request,
                  'blog/post_detail.html',{'post':post, 'url':path, 'comments': comments})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit = False)
            post.author = request.user
            post.publish()
            post.save()
            return redirect('post_detail', slug = post.slug)
    else:
        form = PostForm()
    return render(request,'blog/post_edit.html',{'form': form})

def post_edit(request, slug):
    post = get_object_or_404(Post, slug = slug)
    if request.method == "POST":
        form = PostForm(request.POST, instance = post)
        if form.is_valid:
            post = form.save(commit = False)
            post.author = request.user
            post.created_date = timezone.now()
            post.save()
            return redirect('post_detail', slug = post.slug)
    else:
        
        form = PostForm(instance = post)
    return render(request,'blog/post_edit.html',{'form': form})


def profile(request, username = None):
    if User.objects.get(username=username):
        user = User.objects.get(username = username)
        posts = Post.objects.filter(author = user).order_by('-created_date')
        return render(request, 'registration/dashboard.html',{'posts': posts})
    
    else:
        return render("User not found")

def register(request):
    if request.method == "GET":
        
        return render(request, "registration/register.html", {'form' : UserRegistrationForm})
    elif request.method == "POST":
        
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit = True)
            login(request, user)
            return redirect('profile', username = user.username)

    return redirect('register')

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
    post.delete()
    return redirect('post_list')

def get_note(request, slug):
    post = get_object_or_404(Post, slug = slug)
    path = './media/'+post.note.name
    try:
        return FileResponse(open(path,'rb'), content_type = 'application/pdf')
    except:
        raise Http404()

    