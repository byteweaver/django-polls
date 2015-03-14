"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
import random
import logging
from django.test import TestCase
from django.contrib.auth import get_user
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from polls.models import Poll, Choice, Vote
from polls.exceptions import PollClosed, PollNotOpen, PollNotAnonymous, PollNotMultiple

logger = logging.getLogger(__name__)


# view tests are outdated
class PollsViewTest(TestCase):
    def setUp(self):
        self.username = "user%d" % (random.random() * 100)
        self.user = User.objects.create_user(self.username, 'test@test.com', 'testtest')
        poll, self.cids = create_poll_single()
        self.poll_pk = poll.pk

    def tearDown(self):
        self.client.logout()

    def test_polls_list_view(self):
        self.client.login(username=self.username, password='testtest')
        resp = self.client.get(reverse('polls:list'))
        self.assertEqual(resp.status_code, 200)
        Poll.objects.all().delete()
        resp = self.client.get(reverse('polls:list'))
        self.assertEqual(resp.status_code, 200)

    def test_polls_list_view_anonymous(self):
        user = get_user(self.client)
        self.assertTrue(user.is_anonymous())
        resp = self.client.get(reverse('polls:list'))
        self.assertEqual(resp.status_code, 200)

    def test_detail_view(self):
        self.client.login(username=self.username, password='testtest')
        resp = self.client.get(reverse('polls:detail', args=[self.poll_pk]))
        self.assertEqual(resp.status_code, 200)
        # get nonexistent poll
        resp = self.client.get(reverse('polls:detail', args=[self.poll_pk+1]))
        self.assertEqual(resp.status_code, 404)

    def test_detail_view_anonymous(self):
        user = get_user(self.client)
        self.assertTrue(user.is_anonymous())
        resp = self.client.get(reverse('polls:detail', args=[self.poll_pk]))
        self.assertEqual(resp.status_code, 200)

    def test_vote_view(self):
        self.client.login(username=self.username, password='testtest')
        resp = self.client.post(reverse('polls:vote', args=[self.poll_pk]), {'choice_pk': self.cids[1]})
        self.assertEqual(resp.status_code, 301)
        self.assertEqual(Vote.objects.all().count(), 1)
        # vote again
        resp = self.client.post(reverse('polls:vote', args=[self.poll_pk]), {'choice_pk': self.cids[1]})
        self.assertEqual(resp.status_code, 403)
        self.assertEqual(Vote.objects.all().count(), 1)

    def test_vote_anonymous(self):
        user = get_user(self.client)
        self.assertTrue(user.is_anonymous())
        resp = self.client.post(reverse('polls:vote', args=[1]), {'choice_pk': self.cids[1]})


class PollsModelTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user('user1', 'test1@test.com', 'testtest1')
        self.user2 = User.objects.create_user('user2', 'test2@test.com', 'testtest2')
        self.user3 = User.objects.create_user('user3', 'test3@test.com', 'testtest3')
        self.user4 = User.objects.create_user('user4', 'test4@test.com', 'testtest4')
        Choice.objects.all().delete()

    def tearDown(self):
        pass

    def test_poll_methods(self):
        poll, cids = create_poll_single()
        self.assertEqual(Poll.objects.count(), 1)
        self.assertEqual(poll.count_choices(), 3)

    def test_single_vote(self):
        poll, cids = create_poll_single()
        poll.vote([cids[0]], self.user1)
        self.assertRaises(PollNotMultiple, poll.vote, *([cids[0], cids[1]], self.user2))
        self.assertRaises(PollNotAnonymous, poll.vote, [cids[0]])

    def test_single_vote_stat_1(self):
        poll, cids = create_poll_single()
        poll.vote([cids[0]], self.user1)
        poll.vote([cids[1]], self.user2)
        self.assertEqual(poll.count_percentage(), [0.5, 0.5, 0])

    def test_single_vote_stat_2(self):
        poll, cids = create_poll_single()
        poll.vote([cids[0]], self.user1)
        self.assertEqual(poll.count_percentage(), [1.0, 0, 0])

    def test_single_vote_stat_3(self):
        poll, cids = create_poll_single()
        poll.vote([cids[0]], self.user1)
        poll.vote([cids[1]], self.user2)
        poll.vote([cids[2]], self.user3)
        self.assertEqual(poll.count_percentage(), [1.0/3, 1.0/3, 1.0/3])

    def test_multiple_vote(self):
        poll, cids = create_poll_multiple()
        poll.vote([cids[0],cids[1]], self.user1)
        self.assertRaises(PollNotAnonymous, poll.vote, [cids[1], cids[2]])

    def test_multiple_vote_stat(self):
        poll, cids = create_poll_multiple()
        poll.vote([cids[0],cids[1]], self.user1)
        self.assertEqual(poll.count_percentage(), [0.5, 0.5, 0.0, 0.0, 0.0])
        poll.vote([cids[2],cids[3],cids[4]], self.user2)
        self.assertEqual(poll.count_percentage(), [0.2, 0.2, 0.2, 0.2, 0.2])

    def test_anonymous_single_vote(self):
        poll, cids = create_poll_anonymous_single()
        poll.vote([cids[1]], self.user1)
        poll.vote([cids[1]])
        self.assertRaises(PollNotMultiple, poll.vote, *([cids[0],cids[1]], self.user2))
        self.assertRaises(PollNotMultiple, poll.vote, [cids[0],cids[1]])

    def test_anonymous_single_vote_stat(self):
        poll, cids = create_poll_anonymous_single()
        poll.vote([cids[0]])
        self.assertEqual(poll.count_percentage(), [1.0, 0, 0])
        poll.vote([cids[1]], self.user1)
        poll.vote([cids[2]], self.user2)
        self.assertEqual(poll.count_percentage(), [1.0/3, 1.0/3, 1.0/3])

    def test_anonymous_multiple_vote(self):
        poll, cids = create_poll_anonymous_multiple()
        poll.vote([cids[1]], self.user1)
        poll.vote([cids[1]])
        poll.vote([cids[0], cids[1]], self.user2)
        poll.vote([cids[0],cids[1]])

    def test_anonymous_multiple_vote_stat(self):
        poll, cids = create_poll_anonymous_multiple()
        poll.vote([cids[1]])
        self.assertEqual(poll.count_percentage(), [0.0, 1.0, 0.0, 0.0, 0.0])

# for authenticated users, only one vote allowed
def create_poll_single():
    poll = Poll(question='How are you?', description='description')
    poll.save()
    choices = list()
    choices.append(Choice(poll=poll, choice='I am fine'))
    choices.append(Choice(poll=poll, choice='So so'))
    choices.append(Choice(poll=poll, choice='Bad'))
    [choice.save() for choice in choices]
    return poll, [choice.pk for choice in choices]

# for authenticated users, multiple votes are allowed
def create_poll_multiple():
    poll = Poll(question='Which languages do you know?', description='description', is_multiple=True)
    poll.save()
    choices = list()
    choices.append(Choice(poll=poll, choice='French'))
    choices.append(Choice(poll=poll, choice='English'))
    choices.append(Choice(poll=poll, choice='German'))
    choices.append(Choice(poll=poll, choice='Japanese'))
    choices.append(Choice(poll=poll, choice='Chinese'))
    [choice.save() for choice in choices]
    return poll, [choice.pk for choice in choices]

# for anonymous and authenticated users, only one vote allowed
def create_poll_anonymous_single():
    poll = Poll(question='Are you an anonymous?', description='description', is_anonymous=True)
    poll.save()
    choices = list()
    choices.append(Choice(poll=poll, choice='Yes'))
    choices.append(Choice(poll=poll, choice='No'))
    choices.append(Choice(poll=poll, choice='Nobody knows'))
    [choice.save() for choice in choices]
    return poll, [choice.pk for choice in choices]

# for anonymous and authenticated users, multiple votes are allowed
def create_poll_anonymous_multiple():
    poll = Poll(question='Choose what do you like', description='description', is_anonymous=True, is_multiple=True)
    poll.save()
    choices = list()
    choices.append(Choice(poll=poll, choice='Chocolate'))
    choices.append(Choice(poll=poll, choice='Milk'))
    choices.append(Choice(poll=poll, choice='Fruits'))
    choices.append(Choice(poll=poll, choice='Meat'))
    choices.append(Choice(poll=poll, choice='Vegetables'))
    [choice.save() for choice in choices]
    return poll, [choice.pk for choice in choices]


