from django.views.generic import ListView

from models import Poll


class PollListView(ListView):
    model = Poll
