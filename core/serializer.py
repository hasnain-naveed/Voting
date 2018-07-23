from django.contrib.auth.models import User, Group
from core.models import Candidate, PollingStation, PollingStationVotes
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class CandidateSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = Candidate
        fields = (
            'name',
            'sign',
            'votes'
        )