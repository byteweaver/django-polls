from django.db import models
from django.contrib.auth.models import User


class Poll(models.Model):
    question = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __unicode__(self):
        return self.question


class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    choice = models.CharField(max_length=255)

    def count_votes(self):
        return self.vote_set.count()

    def __unicode__(self):
        return self.choice

    class Meta:
        ordering = ['choice']


class Vote(models.Model):
    user = models.ForeignKey(User)
    poll = models.ForeignKey(Poll)
    choice = models.ForeignKey(Choice)

    def __unicode__(self):
        return u'Vote for %s' % (self.choice)

    class Meta:
        unique_together = (('user', 'poll'))
