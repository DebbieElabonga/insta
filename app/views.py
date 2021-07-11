from django.shortcuts import render,redirect, get_object_or_404
from .models import Profile, Post, Comment,Follow
from django.contrib.auth.models import User
from .forms import PostForm, SignUpForm, UserCreationForm, UpdateUserProfileForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate



# Create your views here.
@login_required(login_url='login')
def welcome(request):
    posts = Post.objects.all()
    return render(request, 'index.html',{"posts":posts})

def comment(request,id):
    all_comments = Comment.get_comments(id)
    return render(request, 'comments.html', {"comments":all_comments})

# def user_profile(request, username):
#     user_prof = get_object_or_404(User, username=username)
#     if request.user == user_prof:
#         return redirect('user_profile', username=request.user.username)
#     user_posts = user_prof.profile.posts.all()
    
#     context = {
#         'user_prof': user_prof,
#         'user_posts': user_posts,
        
#     }
#     return render(request, 'user_profile.html', context)

@login_required(login_url='login')
def upload_image(request):
    posts = Post.objects.all()
    users = User.objects.exclude(id=request.user.id)
    form = PostForm(request.POST or None, files=request.FILES)      
    if form.is_valid():
        post=form.save(commit=False)
        post.user = request.user.profile
        post.save()
        return redirect('index')
    context = {
        'posts': posts,
        'form': form,
        'users':users,
    }
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
def profile(request):
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

@login_required(login_url='login')
def user_profile(request, username):
    user_prof = get_object_or_404(User, username=username)
    if request.user == user_prof:
        return redirect('user_profile', username=request.user.username)
    user_posts = user_prof.profile.posts.all()
    followers = Follow.objects.filter(followers=user_prof.profile)
    follow_status = None
    for follower in followers:
        if request.user.profile == follower.following:

            follow_status = True
        else:
            follow_status = False
    context = {
        'user_prof': user_prof,
        'user_posts': user_posts,
        'followers': followers,
        'follow_status': follow_status
    }
    return render(request, 'user_profile.html', context)

@login_required(login_url="login")
def searchuser(request):
    if 'username' in request.GET and request.GET["username"]:
        search_name = request.GET.get("username")
        searched_profiles = Profile.search_profile(search_name)
        message = f"{search_name}"

        return render(request,"search.html",{"message":message,"searched_profiles":searched_profiles})
    else:
        message = "Enter a username to search"
        return render(request,"search.html",{"message":message})

def follow(request, pk):
    if request.method == 'GET':
        user = Profile.objects.get(pk=pk)
        follow = Follow(following=request.user.profile, followers=user)
        follow.save()
        
    return redirect('user_profile', user.user.username)
    
def unfollow(request, pk):
    if request.method == 'GET':
        user_ = Profile.objects.get(pk=pk)
        unfollow= Follow.objects.filter(following=request.user.profile, followers=user_)
        unfollow.delete()
        return redirect('user_profile', user_.user.username)    
