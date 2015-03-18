'''
    Api("v1/poll")
    POST /poll/ -- create a new poll, shall allow to post choices in the same API call
    POST /choice/ -- add a choice to an existing poll
    POST /vote/ -- vote on poll with pk
    PUT /choice/ -- update choice data
    PUT /poll/ -- update poll data
    GET /poll/ -- retrieve the poll information, including choice details
    GET /result/ -- retrieve the statistics on the poll.
    This shall return a JSON formatted like so. Note the actual statistics calculation shall be implemented
        in poll.service.stats (later on, this will be externalized into a batch job).
'''

from exceptions import PollClosed, PollNotOpen, PollNotAnonymous, PollNotMultiple

from django.conf.urls import url
from django.contrib.auth import get_user_model
from django.core.urlresolvers import resolve
from django.forms.models import model_to_dict
from tastypie import fields
from tastypie import http
from tastypie.authentication import MultiAuthentication, BasicAuthentication, SessionAuthentication
from tastypie.authorization import Authorization, ReadOnlyAuthorization
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.resources import ModelResource, ALL, NamespacedModelResource

from polls.models import Poll, Choice, Vote


class UserResource(NamespacedModelResource):
    def limit_list_by_user(self, request, object_list):
        """
        limit the request object list to its own profile, except
        for superusers. Superusers get a list of all users

        note that for POST requests tastypie internally
        queries get_object_list, and we should return a valid
        list
        """
        view, args, kwargs = resolve(request.path)
        if request.method == 'GET' and not 'pk' in kwargs and not request.user.is_superuser:
            return object_list.filter(pk=request.user.pk)
        return object_list

    def get_object_list(self, request):
        object_list = super(UserResource, self).get_object_list(request)
        object_list = self.limit_list_by_user(request, object_list)
        return object_list
    
    class Meta:
        queryset = get_user_model().objects.all()
        allowed_methods = ['get']
        resource_name = 'user'
        always_return_data = True
        authentication = MultiAuthentication(BasicAuthentication(), SessionAuthentication())
        authorization = ReadOnlyAuthorization()
        excludes = ['date_joined', 'password', 'is_superuser', 'is_staff', 'is_active', 'last_login', 'first_name', 'last_name']
        filtering = {
            'username': ALL,
        }


class PollResource(NamespacedModelResource):
    # POST, GET, PUT
    # user = fields.ForeignKey(UserResource, 'user')
    def obj_create(self, bundle, **kwargs):
        return super(PollResource, self).obj_create(bundle, user=bundle.request.user)
    
    def dehydrate(self, bundle):
        choices = Choice.objects.filter(poll=bundle.data['id'])
        bundle.data['choices'] = [model_to_dict(choice) for choice in choices]
        return bundle

    def alter_detail_data_to_serialize(self, request, data):
        data.data['already_voted'] = Poll.objects.get(pk=data.data.get('id')).already_voted(user=request.user)
        return data
    
    def prepend_urls(self):
        """ match by pk or reference """ 
        return [
            url(r"^(?P<resource_name>%s)/(?P<pk>[0-9]+)/$" % self._meta.resource_name,
                self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
            url(r"^(?P<resource_name>%s)/(?P<reference>[\w-]+)/$" % self._meta.resource_name,
                self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
        ]

    class Meta:
        queryset = Poll.objects.all()
        allowed_methods = ['get', 'post', 'put']
        resource_name = 'poll'
        always_return_data = True
        authentication = MultiAuthentication(BasicAuthentication(), SessionAuthentication())
        authorization = Authorization()


class ChoiceResource(NamespacedModelResource):
    poll = fields.ToOneField(PollResource, 'poll')

    class Meta:
        queryset = Choice.objects.all()
        allowed_methods = ['post', 'put']
        authentication = MultiAuthentication(BasicAuthentication(), SessionAuthentication())
        authorization = Authorization()
        resource_name = 'choice'
        always_return_data = True


class VoteResource(NamespacedModelResource):
    user = fields.ToOneField(UserResource, 'user', blank=True, null=True, readonly=True)
    choice = fields.ToOneField(ChoiceResource, 'choice', readonly=True)
    poll = fields.ToOneField(PollResource, 'poll', readonly=True)
    
    def dispatch(self, *args, **kwargs):
        request = args[1]
        return super(VoteResource, self).dispatch(*args, **kwargs)

    def obj_create(self, bundle, **kwargs):
        poll = PollResource().get_via_uri(bundle.data.get('poll'))
        if not poll.already_voted(bundle.request.user):
            try:
                votes = poll.vote(choices=bundle.data.get('choice'),
                          data=bundle.data.get('data'),
                          user=bundle.request.user)
            except (PollClosed, PollNotOpen, PollNotAnonymous, PollNotMultiple):
                raise ImmediateHttpResponse(response=http.HttpForbidden('not allowed'))
            else:
                bundle.obj = votes[0]
        else:
            raise ImmediateHttpResponse(response=http.HttpForbidden('already voted'))
        return bundle
    
    def obj_update(self, bundle, **kwargs):
        poll = PollResource().get_via_uri(bundle.data.get('poll'))
        # non anonymous votes by the same user can be modified
        if not poll.is_anonymous and bundle.obj.user == bundle.request.user:
            bundle.obj.change_vote(choices=bundle.data.get('choice'),
                          data=bundle.data.get('data'),
                          user=bundle.request.user)
        else:
            raise ImmediateHttpResponse(response=http.HttpForbidden('already voted'))
            
            
    class Meta:
        queryset = Vote.objects.all()
        allowed_methods = ['post', 'put']
        authentication = MultiAuthentication(BasicAuthentication(), SessionAuthentication())
        # authorization = Authorization()
        resource_name = 'vote'
        always_return_data = True


class ResultResource(NamespacedModelResource):
    def prepend_urls(self):
        """ match by pk or reference """ 
        return [
            url(r"^(?P<resource_name>%s)/(?P<pk>[0-9]+)/$" % self._meta.resource_name,
                self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
            url(r"^(?P<resource_name>%s)/(?P<reference>[\w-]+)/$" % self._meta.resource_name,
                self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
        ]
    
    def dehydrate(self, bundle):
        poll = bundle.obj
        percentage = poll.count_percentage()
        count = poll.count_total_votes()
        # FIXME order of labels must be guaranteed to be the same as order stats
        # since we have different db queries here, in Polls, Choices this is
        # not guaranteed. solution: implement consistent Polls.get_stats()
        labels = [choice.choice for choice in Choice.objects.filter(poll=bundle.data['id'])]
        bundle.data['stats'] = dict(values=percentage, labels=labels, votes=count)
        return bundle

    class Meta:
        queryset = Poll.objects.all()
        allowed_methods = ['get']
        authentication = MultiAuthentication(BasicAuthentication(), SessionAuthentication())
        authorization = Authorization()
        resource_name = 'result'
        always_return_data = True
        excludes = ['description', 'start_votes', 'end_votes', 'is_anonymous', 'is_multiple', 'is_closed', 'reference']

