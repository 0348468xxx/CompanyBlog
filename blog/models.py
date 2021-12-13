from django.db import models
from django.core.validators import MinLengthValidator

# Create your models here.


class Tag(models.Model):
    caption = models.CharField(max_length=50)


class Author(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email_address = models.EmailField()


class Post(models.Model):
    title = models.CharField(max_length=100)
    excerpt = models.CharField(max_length=250)
    image_name = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, db_index=True)
    content = models.TextField(validators=[MinLengthValidator(10)])
    author = models.ForeignKey(
        Author, on_delete=models.SET_NULL, related_name="posts")
    tags = models.ManyToManyField(Tag)

    
