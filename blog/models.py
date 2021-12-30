"""
Blog Models is designed on the basis of this document: https://drive.google.com/file/d/1YxtaPHvSEkEnUwldlODPoC0WE4KsfmOv/view?usp=sharing
"""

from django.db import models
from django.core.validators import MinLengthValidator
from django.db.models.deletion import CASCADE
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField 
from django.contrib.auth.models import User


class Tag(models.Model):
    caption = models.CharField(max_length=50)

    def __str__(self):
        return self.caption


class Author(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email_address = models.EmailField()

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name()


class Post(models.Model):
    title = models.CharField(max_length=100)
    excerpt = models.CharField(max_length=250)
    image = models.ImageField(upload_to="posts", null=True)
    date = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, db_index=True)
    content = RichTextUploadingField()
    author = models.ForeignKey(
        Author, on_delete=models.SET_NULL, related_name="posts", null=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title

class Comment(models.Model):
    # user_name = models.CharField(max_length=120)
    # user_emai = models.CharField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    text = RichTextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments")
    parent = models.ForeignKey("self", null=True, blank=True,
        on_delete=models.CASCADE, related_name='+')

    class Meta:
        ordering = ['-timestamp']


    def __str__(self):
        return self.text

    @property
    def children(self):
        return Comment.objects.filter(parent=self).order_by('timestamp').all()

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True