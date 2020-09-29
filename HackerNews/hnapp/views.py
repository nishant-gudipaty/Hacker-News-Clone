from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import ListView
from .models import Post,Vote,Comment
from .forms import CommentForm,PostForm

from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
# Create your views here.


def PostListView(request):
    posts = Post.objects.all()
    for post in posts:
        post.count_votes()
        post.count_comments()
        
    context = {
        'posts': posts,
    }
    return render(request,'hnapp/postlist.html',context)

from datetime import datetime,timedelta
from django.utils import timezone

def NewPostListView(request):
    posts = Post.objects.all().order_by('-created_on')
    for post in posts:
        post.count_votes()
        post.count_comments()    
    context = {
        'posts': posts,
    }
    return render(request,'hnapp/postlist.html', context)


def PastPostListView(request):
    time = str((datetime.now(tz=timezone.utc) - timedelta(minutes=30)))
    posts = Post.objects.filter(created_on__lte = time)
    for post in posts:
        post.count_votes()
        post.count_comments()

    context={
        'posts': posts,
    }
    return render(request,'hnapp/postlist.html',context)

def UpVoteView(request,id):
    if request.user.is_authenticated:
        post = Post.objects.get(id=id)
        votes = Vote.objects.filter(post = post)
        v = votes.filter(voter = request.user)
        if len(v) == 0:
            upvote = Vote(voter=request.user,post=post)
            upvote.save()
            return redirect('/')
    return redirect('/signin')


def DownVoteView(request,id):
    if request.user.is_authenticated:
        post = Post.objects.get(id=id)
        votes = Vote.objects.filter(post = post)
        v = votes.filter(voter = request.user)
        if len(v) != 0:
            v.delete()
            return redirect('/')
    return redirect('/signin')    


def UserInfoView(request,username):
    user = User.objects.get(username=username)
    context = {'user':user,}
    return render(request,'hnapp/userinfo.html',context)


def UserSubmissions(request,username):
    user = User.objects.get(username=username)
    posts = Post.objects.filter(creator = user)
    print(len(posts))
    for post in posts:
        post.count_votes()
        post.count_comments()    
    return render(request,'hnapp/user_posts.html',{'posts': posts})
  
def EditListView(request,id):
    post = get_object_or_404(Post,id=id)
    if request.method =='POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('/')
    
    form = PostForm(instance =post)
    return render(request,'hnapp/submit.html',{'form':form})


def CommentListView(request,id):
    form = CommentForm()
    post = Post.objects.get(id =id)
    post.count_votes()
    post.count_comments()

    comments = []    
    def func(i,parent):
        children = Comment.objects.filter(post =post).filter(identifier =i).filter(parent=parent)
        for child in children:
            gchildren = Comment.objects.filter(post =post).filter(identifier = i+1).filter(parent=child)
            if len(gchildren)==0:
                comments.append(child)
            else:
                func(i+1,child)
                comments.append(child)
    func(0,None)
    print(comments)

    if request.method == "POST":
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                content = form.cleaned_data['content']
                comment = Comment(creator = request.user,post = post,content = content,identifier =0)
                comment.save()
                return redirect(f'/post/{id}')
        return redirect('/signin')
    
    
    context ={
        'form': form,
        'post': post,
        'comments': list(reversed(comments)),
    }
    return render(request,'hnapp/post.html', context)


def CommentReplyView(request,id1,id2):
    form = CommentForm()
    comment = Comment.objects.get(id = id2)
    post = Post.objects.get(id=id1)

    if request.method == "POST":
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            
            if form.is_valid():
                reply_comment_content = form.cleaned_data['content']
                identifier = int(comment.identifier + 1)

                reply_comment = Comment(creator = request.user, post = post, content = reply_comment_content, parent=comment, identifier= identifier)
                reply_comment.save()

                return redirect(f'/post/{id1}')
        return redirect('/signin')
    
    context ={
        'form': form,
        'post': post,
        'comment': comment,
    }
    return render(request,'hnapp/reply_post.html', context)

def SubmitPostView(request):
    if request.user.is_authenticated:
        form = PostForm()

        if request.method == "POST":
            form = PostForm(request.POST)

            if form.is_valid():
                title = form.cleaned_data['title']
                url = form.cleaned_data['url']
                description = form.cleaned_data['description']
                creator = request.user
                created_on = datetime.now()

                post = Post(title=title, url=url, description=description, creator = creator, created_on=created_on)

                post.save()
                return redirect('/')
        return render(request,'hnapp/submit.html',{'form':form})
    return redirect('/signin')

from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm

def signup(request):

    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username = username,password = password)
            login(request, user)
            return redirect('/')
        
        else:
            return render(request,'hnapp/auth_signup.html',{'form':form})
    
    else:
        form = UserCreationForm()
        return render(request,'hnapp/auth_signup.html',{'form':form})


def signin(request):
    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username =username, password = password)

        if user is not None:
            login(request,user)
            return redirect('/')
        else:
            form = AuthenticationForm()
            return render(request,'hnapp/auth_signin.html',{'form':form})
    
    else:
        form = AuthenticationForm()
        return render(request, 'hnapp/auth_signin.html', {'form':form})


def signout(request):
    logout(request)
    return redirect('/')