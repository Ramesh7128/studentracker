from django.db import models
from django.contrib.auth.models import User

# Create your models here.

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





