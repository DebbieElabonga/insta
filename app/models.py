from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField
from django.db.models.signals import post_save
from django.dispatch import receiver



# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True, default='No bio')
    profile = models.ImageField(upload_to='images/', default='default.jpeg')
    
    def save_profile(self):
        self.save()

    @classmethod
    def search_profile(cls,name):
        return cls.objects.filter(user__username__icontains=name).all()
    def __str__(self):
        return self.user.username


class Post(models.Model):
    image = models.ImageField(upload_to='posts/')
    name = models.CharField(max_length=250, blank=True)
    caption = models.CharField(max_length=250, blank=True)
    date = models.DateTimeField(auto_now_add=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    likes = models.ManyToManyField(User, related_name='likes', blank=True, )
    
    class Meta:
        ordering = ["-pk"]

    def save_image(self):
        self.save()

    def get_absolute_url(self):
        return f"/post/{self.id}"
    
    def delete_image(self):
        self.delete()
    

    def __str__(self):
        return self.name

    def total_likes(self):
        return self.likes.count()

class Follow(models.Model):
    following = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='following')
    followers = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='followers')
   
    def __str__(self):
        return self.following


class Comment(models.Model):
    comment = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='comments')
    created = models.DateTimeField(auto_now_add=True, null=True)

    def save_comment(self):
        self.save()
        
    def __str__(self):
        return self.comment
    def delete_comment(self):
        self.delete()
    
    @classmethod
    def get_comments(cls,image_id):
        return cls.objects.filter(post=image_id).all()

    class Meta:
        ordering = ["-pk"]

    




