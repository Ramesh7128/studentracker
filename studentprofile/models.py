from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    picture = models.ImageField(upload_to='profile_images', blank="True")

    def __unicode__(self):
        return self.user.username

class profile(models.Model):
    users = models.ForeignKey(User)
    github = models.URLField()
    codecademy = models.URLField()
    teamtreehouse = models.URLField()
    codewars = models.URLField()

    def __unicode__(self):
        return self.users

class stacklistmodel(models.Model):
    users = models.ForeignKey(User)
    stack = models.CharField(max_length=50)
    parentid = models.IntegerField()
    value = models.IntegerField()
    colors = models.CharField(max_length=50)

    def __unicode__(self):
        return self.stack

class Githubmodel(models.Model):
    users = models.ForeignKey(User)
    reponame = models.CharField(max_length=100)
    stack = models.CharField(max_length=50)
    bytes = models.IntegerField()

    def __unicode__(self):
        return self.reponame

class CodeCademymodel(models.Model):
    users = models.ForeignKey(User)
    coursename = models.CharField(max_length=100)

    def __unicode__(self):
        return self.coursename

class TeamTreeHousemodel(models.Model):
    users = models.ForeignKey(User)
    coursename = models.CharField(max_length=100)
    points = models.IntegerField()

    def __unicode__(self):
        return self.coursename


class Codewarsmodel(models.Model):
    users = models.ForeignKey(User)
    language = models.CharField(max_length=50)
    honors = models.IntegerField()
    rank = models.CharField(max_length=40)
    completedchallenges = models.IntegerField()

    def __unicode__(self):
        return self.language