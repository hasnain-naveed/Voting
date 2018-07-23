# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from core.models import Candidate, PollingStation, PollingStationVotes


admin.site.register(Candidate)
admin.site.register(PollingStation)
admin.site.register(PollingStationVotes)