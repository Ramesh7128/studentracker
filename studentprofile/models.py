from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class profile(models.Model):
    users = models.ForeignKey(User)
    github = models.URLField()
    codecademy = models.URLField()
    teamtreehouse = models.URLField()

    def __unicode__(self):
        return self.users.username





