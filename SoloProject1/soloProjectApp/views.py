from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt


# main page
def index(request):
    return render(request, 'index.html')


# login validations
def login(request):
    user = User.objects.filter(username=request.POST['username'])
    if user:
        userLogin = user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), userLogin.password.encode()):
            request.session['user_id'] = userLogin.id
            return redirect('/gallery/')
        messages.error(request, 'Invalid Credentials')
        return redirect('/')
    messages.error(
        request, 'The username is not in our system, please register for an account')
    return redirect('/')


def users(request):
    if request.method == "GET":
        return redirect('/register')
    errors = User.objects.validate(request.POST)
    if errors:
        for err in errors.values():
            messages.error(request, err)
        return redirect('/register')
    hashedPW = bcrypt.hashpw(
        request.POST['password'].encode(), bcrypt.gensalt()).decode()
    newUser = User.objects.create(
        username=request.POST['username'],
        first_name=request.POST['first_name'],
        last_name=request.POST['last_name'],
        email=request.POST['email'],
        password=hashedPW,
        confirm_pw=hashedPW,
    )
    request.session['user_id'] = newUser.id
    return redirect('/gallery/')

# registration


def newUser(request):
    return render(request, 'registration.html')


def gallery(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'user': user,
    }
    return render(request, 'indexgallery.html', context)


def logout(request):
    request.session.clear()
    return redirect('/')


def menu(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'user': user,
    }
    return render(request, 'restaurantMenu.html', context)


def add_like(request, id):
    liked_message = User.objects.get(id=id)
    user_liking = User.objects.get(id=request.session['user_id'])
    liked_message.user_likes.add(user_liking)

    return redirect('/menu/')


def userProfile(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'user': user,
    }
    return render(request, 'profile.html', context)


def editProfile(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'user': user,
    }
    return render(request, 'profile.html', context)


def updateProfile(request, user_id):
    userProfile = User.objects.get(id=request.session['user_id'])
    userProfile.first_name = request.POST['first_name']
    userProfile.last_name = request.POST['last_name']
    userProfile.username = request.POST['username']
    userProfile.email = request.POST['email']
    userProfile.save()

    return redirect(f'/userProfile')
