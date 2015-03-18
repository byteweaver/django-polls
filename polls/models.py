from datetime import timedelta
from exceptions import PollClosed, PollNotOpen, PollNotAnonymous, PollNotMultiple
from uuid import uuid4

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.fields.json import JSONField 

from polls.exceptions import PollChoiceRequired, PollInvalidChoice


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

    def vote(self, choices, user=None, data=None):
        current_time = timezone.now()
        if self.is_closed:
            raise PollClosed
        if current_time < self.start_votes or current_time > self.end_votes:
            raise PollNotOpen
        if user is None and not self.is_anonymous:
            raise PollNotAnonymous
        if not choices:
            raise PollInvalidChoice 
        if len(choices) > 1 and not self.is_multiple:
            raise PollNotMultiple
        if len(choices) == 0:
            raise PollChoiceRequired
        # if self.is_anonymous: user = None # pass None, even though user is authenticated
        votes = []
        for choice_id in choices:
            if isinstance(choice_id, int) or choice_id.isdigit():
                query = dict(pk=choice_id)
            else:
                query = dict(poll=self, code=choice_id)
            try: 
                choice = Choice.objects.get(**query)
            except:
                raise PollInvalidChoice
            if self.is_anonymous:
                user = None
            vote = Vote.objects.create(poll=self, user=user, choice=choice, data=data)
            votes.append(vote)
        return votes
    
    def change_vote(self, choices, user=None, data=None):
        """
        this deletes all previous votes of the user and revotes with
        new choices.
        """
        votes = self.vote_set.filter(user=user).delete()
        self.vote(choices, user=user, data=data)
        return votes

    def count_choices(self):
        return self.choice_set.count()

    def count_percentage(self, as_code=False):
        """
        return a dict of choices and percentages
        {
          <choice> : percentage
          (...)
        }
        """
        total_votes = self.count_total_votes()
        stats = {}
        for choice in self.choice_set.all():
            key = choice.code if as_code else choice 
            stats[key] = float(choice.count_votes()) / total_votes
        return stats

    def count_total_votes(self):
        votes = sum((choice.count_votes() for choice in self.choice_set.all()))
        return votes
    
    def get_stats(self):
        """
        return a statistics object
        
        returns a dict of 
        {
          labels : [choice, ...],
          codes  : [code, ...],
          percentage : [%, ...],
        }
        """
        # get statistics as dict of { choice : pct } 
        stats = self.count_percentage()
        # convert to same indexed labels, codes, percentages 
        labels = []
        codes = []
        percentage = []
        for c,p in stats.iteritems():
            labels.append(c.choice)
            codes.append(c.code)
            percentage.append(p)
        count = self.count_total_votes() 
        stats = dict(values=percentage, codes=codes, 
                     labels=labels, votes=count)
        return stats

    def already_voted(self, user):
        if not self.is_anonymous:
            if user.is_anonymous():
                raise PollNotAnonymous
            return self.vote_set.filter(user=user).exists()
        else:
            return False

    def __unicode__(self):
        return self.question

    class Meta:
        ordering = ['-start_votes']


class Choice(models.Model):
    #: poll reference
    poll = models.ForeignKey(Poll)
    #: label field
    choice = models.CharField(max_length=255)
    #: code as an alternative to id
    code = models.CharField(max_length=36, default='', blank=True)

    def count_votes(self):
        return self.vote_set.count()

    def __unicode__(self):
        return self.choice
    
    def save(self, *args, **kwargs):
        if not self.code:
            self.code = slugify(unicode(self.choice))
        super(Choice, self).save(*args, **kwargs)
        
    class Meta:
        unique_together = (('poll', 'code'),)
        ordering = ['poll', 'choice']
    
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
        ordering = ['poll', 'choice']
