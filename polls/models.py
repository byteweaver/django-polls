from django.db import models
from django.contrib.auth.models import User


class Poll(models.Model):
    question = models.CharField(max_length=255)
    description = models.TextField()

    def __unicode__(self):
        return self.question


class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    choice = models.CharField(max_length=255)

    def __unicode__(self):
        return self.choice


class Vote(models.Model):
    user = models.ForeignKey(User)
    poll = models.ForeignKey(Poll)
    choice = models.ForeignKey(Choice)
