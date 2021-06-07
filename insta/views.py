from . import models
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    posts = Posts.objects.all()
    return render(request, "insta/index.html", {
        "posts": posts
    })

@login_required(login_url='login')
def create(request):
    if request.method == "POST":
        post = Posts(
            owner = request.user.username,
            image = request.POST["image"],
            caption = request.POST["caption"]
        )
        post.save()
        return HttpResponseRedirect(reverse("index"))
    return render(request, "insta/create.html")

def account(request, username):
    posts = Posts.objects.filter(owner = username)
    return render(request, "insta/account.html", {
        "posts": posts,
        "user": username
    })

@login_required(login_url='login')
def like(request, post_id):
    if request.method == "POST":
        posts = Posts.objects.filter(id = post_id)
        for post in posts:
            likes = post.like + 1
            post.objects.update(likes = likes)
        return HttpResponseRedirect(reverse("index"))

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "insta/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "insta/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "insta/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "insta/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "insta/register.html")