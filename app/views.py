from django.shortcuts import render,redirect, get_object_or_404
from .models import Profile, Post, Comment, Follow
from django.contrib.auth.models import User
from .forms import PostForm, SignUpForm, UserCreationForm, UpdateUserProfileForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required

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

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

@login_required(login_url='login')
def profile(request, username):
    images = request.user.profile.posts.all()
    if request.method == 'POST':
        prof_form = UpdateUserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if prof_form.is_valid():
            prof_form.save()
            return redirect(request.path_info)
    else:
        prof_form = UpdateUserProfileForm(instance=request.user.profile)
    context = {
        'prof_form': prof_form,
        'images': images,

    }
    return render(request, 'profile.html', context)