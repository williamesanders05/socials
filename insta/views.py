from . import models
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
# Opening page view
def index(request):
    # Getting all of the posts from the model
    posts = Posts.objects.all()
    # returning the posts in a html file
    return render(request, "insta/index.html", {
        "posts": posts
    })

@login_required(login_url='login')
# view for creating posts
# first we check if the view is posting
# then we make the model fields the inputs of the user and save the new model
#lastly we redirect to index
def create(request):
    if request.method == "POST":
        post = Posts(
            owner = request.user.username,
            image = request.POST["image"],
            caption = request.POST["caption"]
        )
        post.save()
        return HttpResponseRedirect(reverse("index"))
    # this is what you first see when loading the page up
    return render(request, "insta/create.html")

# view for showing a users account
# first we filter through the model for the posts in which the owner matches the account we clicked on
# then we show an html page where the posts on that page are all of the filtered ones
def account(request, username):
    posts = Posts.objects.filter(owner = username)
    return render(request, "insta/account.html", {
        "posts": posts,
        "usera": username
    })

# view for liking posts
# first we check that the form is posting then filter therough the model to find the post with the same id as the one we are given
# We then add 1 to the number of likes on the post and update it, finally you are redirected to the index view
@login_required(login_url='login')
def like(request, post_id):
    if request.method == "POST":
        posts = Posts.objects.filter(id = post_id)
        for post in posts:
            likes = post.likes + 1
            Posts.objects.update(likes = likes)
        return HttpResponseRedirect(reverse("index"))

# view for saving posts
# first we check that the for is posting and then we make a new saved model where the user is the username that is logged in and the post is the id that we get from a hidden input in html
# we then save the new model and redirect to saved page which shows all of your saved posts
@login_required(login_url='login')
def saved(request):
    if request.method == "POST":
        saved = Saved(
            users = request.user.id,
            post = request.POST["postid"]
        )
        saved.save()
        return HttpResponseRedirect(reverse("saved"))
    users = request.user.id
    return render(request, "insta/saved.html", {
        'saves': Saved.objects.filter(users = users),
        'posts': Posts.objects.all()
    })


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