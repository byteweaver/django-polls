from django.views.generic import DetailView, ListView, RedirectView
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

from models import Choice, Poll, Vote


class PollListView(ListView):
    model = Poll


class PollDetailView(DetailView):
    model = Poll

    def get_context_data(self, **kwargs):
        context = super(PollDetailView, self).get_context_data(**kwargs)
        context['poll'].votable = self.object.can_vote(self.request.user)
        return context


class PollVoteView(RedirectView):
    def post(self, request, *args, **kwargs):
        poll = Poll.objects.get(id=kwargs['pk'])
        user = request.user
        choice = Choice.objects.get(id=request.POST['choice_pk'])
        Vote.objects.create(poll=poll, user=user, choice=choice)
        messages.success(request, _("Thanks for your vote."))
        return super(PollVoteView, self).post(request, *args, **kwargs)

    def get_redirect_url(self, **kwargs):
        return reverse_lazy('polls:detail', args=[kwargs['pk']])
