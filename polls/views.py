from django.views.generic import DetailView, ListView, RedirectView
from django.core.urlresolvers import reverse_lazy

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
    def get_redirect_url(self, **kwargs):
        return reverse_lazy('polls:detail', args=[kwargs['pk']])
