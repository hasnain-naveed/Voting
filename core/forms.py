# -*- coding: utf-8 -*-
from django import forms
from core.models import PollingStation
from core.utils import get_urdu_polling_station_name


class PollingStationVoteForm(forms.Form):

    polling_station = forms.ChoiceField(choices=[])
    lion = forms.IntegerField(required=True, label="چوھدری محمود الحق")
    bat = forms.IntegerField(required=True, label="عابد حسین چھٹہ")
    arrow = forms.IntegerField(required=True, label="طاھر مسعود")
    rabbit = forms.IntegerField(required=True, label="صباحت بھٹی")
    bowl = forms.IntegerField(required=True, label="تنویر ناصر")
    cup = forms.IntegerField(required=True, label="رانا وکیل")
    crane = forms.IntegerField(required=True, label="نوشین بھٹی")

    def __init__(self, *args, **kwargs):
        super(PollingStationVoteForm, self).__init__(*args, **kwargs)
        self.fields['polling_station'].choices = [(x.id, get_urdu_polling_station_name(x.name)) for x in PollingStation.objects.all()]

