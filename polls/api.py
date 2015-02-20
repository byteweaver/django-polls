from django.contrib.auth import get_user_model
from tastypie import fields
from tastypie.authorization import DjangoAuthorization
from tastypie.authentication import BasicAuthentication
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
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
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()
        excludes = ['date_joined', 'password', 'is_superuser', 'is_staff', 'is_active', 'last_login', 'first_name', 'last_name']
        filtering = {
            'username': ALL,
        }


class PollResource(ModelResource):
    # POST, GET, PUT
    #user = fields.ForeignKey(UserResource, 'user')

    class Meta:
        queryset = Poll.objects.all()
        allowed_methods = ['get','post','put']
        resource_name = 'poll'
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()
        filtering = {
            'user': ALL_WITH_RELATIONS,
            'pub_date': ['exact', 'lt', 'lte', 'gte', 'gt'],
        }


class ChoiceResource(ModelResource):
    class Meta:
        queryset = Choice.objects.all()
        allowed_methods = ['post','put']
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()
        resource_name = 'choice'


class VoteResource(ModelResource):
    class Meta:
        queryset = Vote.objects.all()
        allowed_methods = ['post']
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()
        resource_name = 'vote'


class ResultResource(ModelResource):
    class Meta:
        allowed_methods = ['get']
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()
        resource_name = 'result'