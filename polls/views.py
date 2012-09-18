from django.views.generic import DetailView, ListView

from models import Poll


class PollListView(ListView):
    model = Poll


class PollDetailView(DetailView):
    model = Poll
