from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from .models import *

def index(request):
    context = {
        "register" : Register.objects.all()
    }
    return render(request, "index.html", context)

def adduser(request):
    errors = Register.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        newuser = Register.objects.create(fname=request.POST['fname'],
        lname= request.POST['lname'], 
        email = request.POST['email'], 
        password = pw_hash)
        request.session['loggedinID'] = newuser.id
        messages.success(request, "User successfully Entered!")
        return redirect('/wall')

def login(request):
        errors = Register.objects.validator(request.POST)
        if len(errors) > 0:
                for key, value in errors.items():
                    messages.error(request, value)
                return redirect('/')
        user = Register.objects.filter(email=request.POST['email'])
        logged_user= user[0]
        request.session['loggedinID'] = logged_user.id
        return redirect('/wall')

def wall(request):
    loggedinuser = Register.objects.get(id= request.session['loggedinID'])
    context = {
        "loggedinuser" : loggedinuser,
        "post" : Post.objects.all(),
        "comment" : Comments.objects.all()
    }
    return render(request,"success.html", context)

def post_message(request):
        user = Register.objects.get(id = request.session['loggedinID'])
        message = Post.objects.create(message =request.POST["message"], register = user)
        time = Post.objects.create(created_at = request.POST['created_at'], register = user)
        print(request.POST['message'])
        return redirect('/wall')

def post_comment(request, messageid):
        onemessage = Post.objects.get(id=messageid)
        user = Register.objects.get(id= request.session['loggedinID'])
        comment = Comments.objects.create(comment=request.POST["comment"], register = user, post = onemessage)
        print(request.POST['comment'])
        return redirect('/wall')

def destroy(request):
    request.session.clear()
    return redirect("/")

