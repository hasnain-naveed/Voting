# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel
from core.utils import get_urdu_polling_station_name


class Candidate(TimeStampedModel):
    name = models.CharField(max_length=128, unique=True, null=False, blank=False, verbose_name=_('Candidate Name'))
    sign = models.CharField(max_length=128, unique=True, null=False, blank=False, verbose_name=_('Candidate Sign'))
    image_name = models.CharField(max_length=128, null=True, blank=True, verbose_name=_('Candidate Imag Name'))
    votes = models.IntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return "Name:{}----Votes: {}".format(self.name, self.votes)

    class Meta:
        verbose_name = _('Candidate')
        verbose_name_plural = _('Candidates')


class PollingStation(TimeStampedModel):
    name = models.CharField(max_length=128, unique=True, null=False, blank=False, verbose_name=_('Polling Station Name'))
    address = models.CharField(max_length=128, null=True, blank=True, verbose_name=_('Polling Station Address'))
    total_votes = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Polling Station')
        verbose_name_plural = _('Polling Stations')


class PollingStationVotes(TimeStampedModel):
    candidate = models.ForeignKey(Candidate, db_index=True, on_delete=models.CASCADE)
    polling_station = models.ForeignKey(PollingStation, db_index=True, on_delete=models.CASCADE)
    votes = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return "candidate:{}----ps:{}----votes:{}".format(self.candidate.name, self.polling_station.name, self.votes)

    class Meta:
        verbose_name = _('Polling Station Votes')
        verbose_name_plural = _('Polling Station Votes')