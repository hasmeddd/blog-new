import random
import re
import unidecode
from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.

# Hàm cus_slugify với tham số tùy chọn add_random
def cus_slugify(text, add_random=True):
    text = unidecode.unidecode(text).lower()
    slug = re.sub(r'[\W_]+', '-', text).strip('-')
    if add_random:
        random_number = random.randint(10000, 99999)
        return f"{slug}-{random_number}"
    return slug

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email',  'first_name', 'last_name','password1', 'password2']
    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        # Thêm class 'form-control' cho từng trường
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'id': 'form3Example1c'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'id': 'form3Example3c'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control', 'id': 'form3Example1f'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control', 'id': 'form3Example1l'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'id': 'form3Example4c'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'id': 'form3Example4cd'})

class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
    
    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'id': 'form3Example1c'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'id': 'form3Example3c'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control', 'id': 'form3Example1f'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control', 'id': 'form3Example1l'})
        
class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = cus_slugify(self.name, add_random=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    STATUS = {
            ('0', "Bản nháp",),
            ('1', "Công khai")
    }

    SECTION = {
        ('Recent', 'Gần đây'),
        ('Popular', 'Phổ biến'),
    }

    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    image = models.ImageField(upload_to="images")
    content = RichTextUploadingField()
    category = models.ForeignKey(Category, related_name='category', on_delete=models.CASCADE)
    post_slug = models.SlugField(unique=True, null=True, blank=True, max_length=200)  
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=STATUS, max_length=1, default=0)
    section = models.CharField(choices=SECTION, max_length=100)
    Main_post = models.BooleanField(default=False)
    saved_by = models.ManyToManyField(User, related_name='saved_blogs', blank=True)
    liked_by = models.ManyToManyField(User, related_name='liked_posts', blank=True)
# for post views
    views = models.PositiveBigIntegerField(default=0)
    def save(self, *args, **kwargs):
        if not self.post_slug:
            # Gọi cus_slugify với số ngẫu nhiên
            self.post_slug = cus_slugify(self.title, add_random=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.category})"

class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='comments')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    comment = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
    
class PostVersion(models.Model):
    version_id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, related_name='versions', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    content = RichTextUploadingField()
    category = models.ForeignKey(Category, related_name='version_category', on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    version_number = models.IntegerField(default=1)
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='post_versions')
    
    def __str__(self):
        return f"{self.post.title} - Phiên bản {self.version_number}"
    
    class Meta:
        ordering = ['-version_number']

    