from django.db import models


class Poll(models.Model):
    question = models.CharField(max_length=255)

    def __unicode__(self):
        return self.question

class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    choice = models.CharField(max_length=255)

    def __unicode__(self):
        return self.choice
