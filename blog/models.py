from django.db import models

# Create your models here.

from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify 
from django.core.files.storage import FileSystemStorage
from .validators import validate_file_extension, validate_image_extension
from django.contrib.auth.models import User
from django.urls import reverse 
from taggit.managers import TaggableManager

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name='myposts')
    title = models.CharField(max_length = 200)
    text = models.TextField()
    created_date = models.DateTimeField(default = timezone.now)
    note = models.FileField(upload_to='media', validators=[validate_file_extension])
    slug = models.SlugField(max_length=255, unique=True)
    tags = TaggableManager(blank=True)
    upvotes = models.IntegerField(default=0)

    class Meta:
        ordering = ('-created_date','upvotes')

    def publish(self):
        self.created_date = timezone.now()
        if not self.slug:
            self.slug = slugify(self.author.username + '-' + self.title)
        self.save()


    def __str__(self):
        return self.title

    def get_votecount(self, type):
        votecount = 0
        if type == "upvote":
            votecount = self.votes.filter(score=1).count()
        else:
            votecount = self.votes.filter(score=2).count()
        
        return votecount


class Comment(models.Model):
    post = models.ForeignKey('blog.Post', on_delete = models.CASCADE, related_name = 'comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=400)
    created_date = models.DateTimeField(default = timezone.now)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null = True, blank = True, related_name='replies')
    
    class Meta:
        # sort comments in chronological order by default
        ordering = ('-created_date',)
    def __str__(self):
        return self.text


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    following = models.ManyToManyField('self',  blank=True, related_name='followers', symmetrical=False)
    tags = TaggableManager(blank = True)
    created_date = models.DateTimeField(default = timezone.now)
    dp = models.ImageField(upload_to='images', default = 'default.png', validators=[validate_image_extension])


class Vote(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name = 'votes')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
