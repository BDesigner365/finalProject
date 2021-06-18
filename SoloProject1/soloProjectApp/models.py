from django.db import models
from django.core.validators import RegexValidator
import re
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import User
from django.db.models.signals import post_save

alphanumeric = RegexValidator(
    r'^[0-9a-zA-Z]*$',  'Only alphanumeric characters are allowed.')


class UserManager(models.Manager):
    def validate(self, form):
        errors = {}
        if len(form['first_name']) < 2:
            errors['first_name'] = 'Please have at least 2 characters in the first name'
        #
        if len(form['last_name']) < 2:
            errors['last_name'] = 'Please have at least 2 characters in the last name'
        #
        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        #
        if not EMAIL_REGEX.match(form['email']):
            errors['email'] = 'Invalid Email Format'
        #
        emailCheck = self.filter(email=form['email'])
        if emailCheck:
            errors['email'] = 'Email is already in use'
        usernameCheck = self.filter(username=form['username'])
        if usernameCheck:
            errors['username'] = 'Username already in use'
        #
        if len(form['password']) < 5:
            errors['password'] = 'Password must be at least 5 characters long'
        #
        if form['password'] != form['confirm_pw']:
            errors['password'] = 'Password does not match'
        #
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=45, null=True)
    last_name = models.CharField(max_length=45, null=True)
    username = models.CharField(max_length=255, null=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=45)
    confirm_pw = models.CharField(max_length=45)
    objects = UserManager()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username


class Login(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=45)
