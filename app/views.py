from django.shortcuts import render,redirect, get_object_or_404
from .models import Profile, Post, Comment, Follow
from django.contrib.auth.models import User
from .forms import PostForm

# Create your views here.
def welcome(request):
    posts = Post.objects.all()
    return render(request, 'index.html',{"posts":posts})

def comment(request,id):
    all_comments = Comment.get_comments(id)
    return render(request, 'comments.html', {"comments":all_comments})

def user_profile(request, username):
    user_prof = get_object_or_404(User, username=username)
    if request.user == user_prof:
        return redirect('user_profile', username=request.user.username)
    user_posts = user_prof.profile.posts.all()
    
    context = {
        'user_prof': user_prof,
        'user_posts': user_posts,
        
    }
    return render(request, 'user_profile.html', context)


def upload_image(request):
    current_user = request.user
    if request.method == 'POST':
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.user = current_user
            image.save()
        return redirect('index')
    else:
        form = PostForm()
    return render(request,'create_post.html',{"form":form})
