from django.conf.urls.defaults import patterns, url
from django.contrib.auth.decorators import login_required

from views import PollDetailView, PollListView, PollVoteView


urlpatterns = patterns('',
    url(r'^$', PollListView.as_view(), name='list'),
    url(r'^(?P<pk>\d+)/$', PollDetailView.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)/vote/$', login_required(PollVoteView.as_view()), name='vote'),
)
