from django.db import models

# Create your models here.

from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify 
from django.core.files.storage import FileSystemStorage
from .validators import validate_file_extension


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    title = models.CharField(max_length = 200)
    text = models.TextField()
    created_date = models.DateTimeField(default = timezone.now)
    note = models.FileField(validators=[validate_file_extension])
    slug = models.SlugField(max_length=255, unique=True)

    def publish(self):
        self.created_date = timezone.now()
        if not self.slug:
            self.slug = slugify(self.author.username + '-' + self.title)
        self.save()


    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey('blog.Post', on_delete = models.CASCADE, related_name = 'comments')
    author = models.CharField(max_length = 50)
    text = models.CharField(max_length=400)
    created_date = models.DateTimeField(default = timezone.now)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null = True, blank = True, related_name='replies')
    
    class Meta:
        # sort comments in chronological order by default
        ordering = ('-created_date',)
    def __str__(self):
        return self.text