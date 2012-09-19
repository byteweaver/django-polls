from django.views.generic import DetailView, ListView, RedirectView

from models import Poll


class PollListView(ListView):
    model = Poll


class PollDetailView(DetailView):
    model = Poll

    def get_context_data(self, **kwargs):
        context = super(PollDetailView, self).get_context_data(**kwargs)
        context['poll'].votable = self.object.can_vote(self.request.user)
        return context


class PollVoteView(RedirectView):
    pass
