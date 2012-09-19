from django.conf.urls.defaults import patterns, url

from views import PollDetailView, PollListView, PollVoteView


urlpatterns = patterns('',
    url(r'^$', PollListView.as_view(), name='list'),
    url(r'^(?P<pk>\d+)/$', PollDetailView.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)/vote/$', PollVoteView.as_view(), name='vote'),
)
