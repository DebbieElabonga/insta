from django.shortcuts import render
from .models import Profile, Post, Comment, Follow
# Create your views here.
def welcome(request):
    posts = Post.objects.all()
    return render(request, 'index.html',{"posts":posts})

def comment(request,id):
    all_comments = Comment.get_comments(id)
    return render(request, 'comments.html', {"comments":all_comments})