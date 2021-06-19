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
    path = '/media/' +  post.note.name
    return render(request,
                  'blog/post_detail.html',{'post':post, 'url':path})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid:
            post = Post(title=request.POST.get('title', False), text=request.POST.get('text',False),note=request.FILES.get('note',False))
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
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(parent__isnull=True)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            parent_obj = None 
            # get parent comment id 
            try:
                parent_id = int(request.POST.get('parent_id'))
            except:
                parent_id = None
            
            if parent_id: 
                    parent_obj = Comment.objects.get(id=parent_id)
                    if parent_obj:
                        reply = form.save(commit=False)
                        reply.parent = parent_obj

            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', slug=post.slug)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form}) 

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

    