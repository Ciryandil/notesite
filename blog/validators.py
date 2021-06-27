import os
from django.core.exceptions import ValidationError

def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.pdf']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')

# def validate_unique_title(value,user):
#     posts = Post.objects.filter(title=value,user=user)
#     if posts:
#         raise ValidationError('Post with same name already exists')