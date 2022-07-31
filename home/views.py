from django.shortcuts import render, redirect
from .models import Blog, ContactModel, BlogComment
from django.contrib.auth.models import User
from django.contrib import messages
import datetime
from django.contrib.auth import authenticate, login, logout
from home.templatetags import extras

def home(request):
    context = {'posts': Blog.objects.all()}
    return render(request, 'home.html', context=context)

def post_detail(request, slug):
    post = Blog.objects.filter(slug=slug).first()
    comments = BlogComment.objects.filter(post=post, parent=None)
    replies = BlogComment.objects.filter(post=post).exclude(parent=None)
    replyDict = {}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno] = [reply]
        else:
            replyDict[reply.parent.sno].append(reply)

    context = {'post': post, 'comments': comments, 'replyDict': replyDict}
    return render(request, 'read_post.html', context=context)

def about_us(request):
    return render (request, 'about.html')

def contact_us(request):
    if request.method == "POST":
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']

        contact_form = ContactModel(email=email, subject=subject, message=message)
        contact_form.save()
        messages.success(request, "Your message sent Sucessfully!!")
        return redirect('contact_us')
    return render (request, 'contact.html')

def search(request):
    query = request.GET['query']
    allposts = Blog.objects.filter(title__icontains=query)
    params = {'posts': allposts}
    return render(request, 'search.html', params)

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']
        
        user = authenticate(username=username, password=pass1)
        
        if user is not None:
            login(request, user)
            fname = user.first_name
            messages.success(request, "Logged In Sucessfully!!")
            return redirect('home')
        else:
            messages.error(request, "Bad Credentials!!")
            return redirect('login')
    
    return render(request, "login.html")

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['useremail']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try some other username.")
            return redirect('signup')
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return redirect('signup')

        if len(username)>20:
            messages.error(request, "Username must be under 20 charcters!!")
            return redirect('signup')
        
        if pass1 != pass2:
            messages.error(request, "Passwords didn't matched!!")
            return redirect('signup')
        
        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!!")
            return redirect('signup')
        
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.is_active = True
        myuser.save()
        messages.success(request, "Your Account has been created succesfully!!")
        return redirect('login')

    return render(request, 'signup.html')

def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('home')

def postComment(request):
    if request.method == "POST":
        comment = request.POST.get("comment")
        user = request.user
        postSlug = request.POST.get("postSlug")
        post = Blog.objects.get(slug=postSlug)
        parentsno = request.POST.get("parentsno")
        if parentsno == "":
            comment = BlogComment(comment=comment, user=user, post=post)
        else:
            parent = BlogComment.objects.get(sno=parentsno)
            comment = BlogComment(comment=comment, user=user, post=post, parent=parent)
        comment.save()
        messages.success(request, "Your reply has been posted Successfully!")
        
    return redirect(f"post-detail/{postSlug}")

