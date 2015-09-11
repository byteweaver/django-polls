from django.test import TestCase

from polls.models import Poll


class PollTests(TestCase):
    def test_model_creation(self):
        p = Poll.objects.create()
        self.assertIsInstance(p, Poll)
