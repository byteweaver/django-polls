import sys
from django.test import TestCase

from polls.models import Poll


class PollTests(TestCase):
    def setUp(self):
        self.poll = Poll.objects.create(
            question='How are you?'
        )

    def test_model_creation(self):
        self.assertIsNotNone(self.poll)
        self.assertIsInstance(self.poll, Poll)

    def test_model_save(self):
        self.poll.save()
        self.assertIsNotNone(self.poll.pk)
        self.assertTrue(self.poll.pk > 0)

    def test_to_string(self):
        if sys.version_info > (3,):
            self.assertEquals(str(self.poll), 'How are you?')
        else:
            self.assertEquals(unicode(self.poll), 'How are you?')
