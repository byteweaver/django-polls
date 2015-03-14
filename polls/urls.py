from django.conf.urls import patterns, url, include
from django.contrib.auth.decorators import login_required

from views import PollDetailView, PollListView, PollVoteView
from tastypie.api import Api
from polls.api import UserResource, PollResource, ChoiceResource, VoteResource, ResultResource

v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(PollResource())
v1_api.register(ChoiceResource())
v1_api.register(VoteResource())
v1_api.register(ResultResource())

urlpatterns = patterns('',
    url(r'^$', PollListView.as_view(), name='list'),
    url(r'^api/', include(v1_api.urls)),
    url(r'^(?P<pk>\d+)/$', PollDetailView.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)/vote/$', login_required(PollVoteView.as_view()), name='vote'),
)
