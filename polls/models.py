from datetime import datetime, timedelta
from django.db import models
from django_extensions.db.fields import UUIDField
from django_extensions.db.fields.json import JSONField
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class Poll(models.Model):
    question = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    reference = UUIDField(max_length=20, version=4)
    is_anonymous = models.BooleanField(default=False, help_text=_('Allow to vote for anonymous user'))
    is_multiple = models.BooleanField(default=False, help_text=_('Allow to make multiple choices'))
    is_closed = models.BooleanField(default=False, help_text=_('Do not accept votes'))
    start_votes = models.DateTimeField(default=datetime.today, help_text=_('The earliest time votes get accepted'))
    end_votes = models.DateTimeField(default=(lambda: datetime.today()+timedelta(days=5)),
                                     help_text=_('The latest time votes get accepted'))

    def count_choices(self):
        return self.choice_set.count()

    def count_total_votes(self):
        result = 0
        for choice in self.choice_set.all():
            result += choice.count_votes()
        return result

    def can_vote(self, user):
        return not self.vote_set.filter(user=user).exists()

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

    class Meta:
        ordering = ['choice']


class Vote(models.Model):
    user = models.ForeignKey(User)
    poll = models.ForeignKey(Poll)
    choice = models.ForeignKey(Choice)
    comment = models.TextField(max_length=144, blank=True, null=True)
    datetime = models.DateTimeField(auto_now_add=True)
    data = JSONField(blank=True, null=True)

    def __unicode__(self):
        return u'Vote for %s' % self.choice

    class Meta:
        unique_together = ('user', 'poll')
