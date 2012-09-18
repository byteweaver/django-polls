from django.conf.urls.defaults import patterns, url

from views import PollListView

urlpatterns = patterns('',
    url(r'^$', PollListView.as_view(), name='list'),
)
