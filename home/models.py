from pyexpat import model
from sqlite3 import Timestamp
from statistics import mode
from django.db import models
from matplotlib.image import thumbnail
from .helpers import *
from froala_editor.fields import FroalaField
from django.contrib.auth.models import User
from slugify import slugify
from django.utils.timezone import now

class Blog(models.Model):
    title = models.CharField(max_length=1000)
    content = FroalaField()
    slug = models.SlugField(max_length=1000, null=True, blank=True)
    thumbnail = models.ImageField(upload_to='img')
    created_at = models.DateTimeField(auto_now_add=True)
    upload_to = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = generate_slug(self.title)
        super(Blog, self).save(*args, **kwargs )

class ContactModel(models.Model):
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()

    def __str__(self):
        return self.email

class BlogComment(models.Model):
    sno = models.AutoField(primary_key=True)
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Blog, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    Timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return self.comment[0:16] + "... " + "by" + self.user.username