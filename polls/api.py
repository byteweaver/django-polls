from django.contrib.auth import get_user_model
from django.forms.models import model_to_dict
from tastypie import fields
from tastypie.authorization import DjangoAuthorization
from tastypie.authentication import SessionAuthentication
from tastypie.resources import ModelResource, Resource, ALL, ALL_WITH_RELATIONS
from polls.models import Poll, Choice, Vote


'''
    Api("v1/poll")
    POST /poll/ -- create a new poll, shall allow to post choices in the same API call
    POST /choice/ -- add a choice to an existing poll
    POST /vote// -- vote on poll with pk
    PUT /choice// -- update choice data
    PUT /poll// -- update poll data
    GET /poll// -- retrieve the poll information, including choice details
    GET /result// -- retrieve the statistics on the poll. This shall return a JSON formatted like so. Note the actual statistics calculation shall be implemented in poll.service.stats (later on, this will be externalized into a batch job).
'''


class UserResource(ModelResource):
    class Meta:
        queryset = get_user_model().objects.all()
        allowed_methods = ['get']
        resource_name = 'user'
        always_return_data = True
        authentication = SessionAuthentication()
        authorization = DjangoAuthorization()
        excludes = ['date_joined', 'password', 'is_superuser', 'is_staff', 'is_active', 'last_login', 'first_name', 'last_name']
        filtering = {
            'username': ALL,
        }


class PollResource(ModelResource):
    # POST, GET, PUT
    #user = fields.ForeignKey(UserResource, 'user')
    def dehydrate(self, bundle):
        choices = Choice.objects.filter(poll=bundle.data['id'])
        bundle.data['choices']  = [model_to_dict(choice) for choice in choices]
        return bundle

    class Meta:
        queryset = Poll.objects.all()
        allowed_methods = ['get','post','put']
        resource_name = 'poll'
        always_return_data = True
        authentication = SessionAuthentication()
        authorization = DjangoAuthorization()


class ChoiceResource(ModelResource):
    poll = fields.ToOneField(PollResource, 'poll')
    class Meta:
        queryset = Choice.objects.all()
        allowed_methods = ['post','put']
        authentication = SessionAuthentication()
        authorization = DjangoAuthorization()
        resource_name = 'choice'
        always_return_data = True


class VoteResource(ModelResource):
    user = fields.ToOneField(UserResource, 'user')
    choice = fields.ToOneField(ChoiceResource, 'choice')
    poll = fields.ToOneField(PollResource, 'poll')

    def obj_create(self, bundle, **kwargs):
        return super(VoteResource, self).obj_create(bundle, user=bundle.request.user)

    class Meta:
        queryset = Vote.objects.all()
        allowed_methods = ['post']
        authentication = SessionAuthentication()
        authorization = DjangoAuthorization()
        resource_name = 'vote'
        always_return_data = True


class ResultResource(ModelResource):
    def dehydrate(self, bundle):
        percentage = Poll.objects.get(pk=bundle.data['id']).count_percentage()
        labels = [choice.choice for choice in Choice.objects.filter(poll=bundle.data['id'])]
        bundle.data['stats'] = dict(values=percentage, labels=labels, votes=len(labels))
        return bundle

    class Meta:
        queryset = Poll.objects.all()
        allowed_methods = ['get']
        authentication = SessionAuthentication()
        authorization = DjangoAuthorization()
        resource_name = 'result'
        always_return_data = True
        excludes = ['description', 'start_votes', 'end_votes', 'is_anonymous', 'is_multiple', 'is_closed', 'reference']

