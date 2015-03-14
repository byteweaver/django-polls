from datetime import timedelta
from exceptions import PollClosed, PollNotOpen, PollNotAnonymous, PollNotMultiple
from uuid import uuid4

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.fields.json import JSONField 


class Poll(models.Model):
    question = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    reference = models.CharField(max_length=36, default=uuid4, unique=True)
    is_anonymous = models.BooleanField(default=False, help_text=_('Allow to vote for anonymous user'))
    is_multiple = models.BooleanField(default=False, help_text=_('Allow to make multiple choices'))
    is_closed = models.BooleanField(default=False, help_text=_('Do not accept votes'))
    start_votes = models.DateTimeField(default=timezone.now, help_text=_('The earliest time votes get accepted'))
    end_votes = models.DateTimeField(default=(lambda: timezone.now()+timedelta(days=5)),
                                     help_text=_('The latest time votes get accepted'))

    def vote(self, choices, user=None):
        current_time = timezone.now()
        if self.is_closed:
            raise PollClosed
        if current_time < self.start_votes or current_time > self.end_votes:
            raise PollNotOpen
        if user is None and not self.is_anonymous:
            raise PollNotAnonymous
        if len(choices) > 1 and not self.is_multiple:
            raise PollNotMultiple
        # if self.is_anonymous: user = None # pass None, even though user is authenticated
        for choice_id in choices:
            choice = Choice.objects.get(pk=choice_id)
            Vote.objects.create(poll=self, user=user, choice=choice)

    def count_choices(self):
        return self.choice_set.count()

    def count_percentage(self):
        votes = [choice.count_votes() for choice in self.choice_set.all()]
        total_votes = sum(votes)
        if total_votes is 0:
            return [0.0 for vote in votes]
        else:
            return [float(vote)/total_votes for vote in votes]

    def count_total_votes(self):
        result = 0
        for choice in self.choice_set.all():
            result += choice.count_votes()
        return result

    def already_voted(self, user):
        if not user.is_anonymous():
            return self.vote_set.filter(user=user).exists()
        else:
            return False

    def __unicode__(self):
        return self.question

    class Meta:
        ordering = ['-start_votes']


class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    choice = models.CharField(max_length=255)

    def count_votes(self):
        return self.vote_set.count()

    def __unicode__(self):
        return self.choice


class Vote(models.Model):
    user = models.ForeignKey(User, blank=True, null=True)
    poll = models.ForeignKey(Poll)
    choice = models.ForeignKey(Choice)
    comment = models.TextField(max_length=144, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    data = JSONField(blank=True, null=True)

    def __unicode__(self):
        return u'Vote for %s' % self.choice

    class Meta:
        unique_together = ('user', 'poll', 'choice')
