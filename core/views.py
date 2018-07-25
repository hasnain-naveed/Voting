from django.contrib.auth.models import User, Group
from core.json import CANDIDATES, POLLING_STATIONS
from core.utils import get_urdu_candidate_name, get_urdu_polling_station_name, get_lion_votes_string
from core.serializer import UserSerializer, GroupSerializer
from core.models import Candidate, PollingStation, PollingStationVotes
from core.forms import PollingStationVoteForm

from django.shortcuts import render
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from django.shortcuts import redirect
from django.views.generic import View


class AddDataView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "all_candidates.html"

    def add_candidate_data(self):
        for candidate in CANDIDATES:
            Candidate.objects.get_or_create(
                name=candidate.get('name'),
                sign=candidate.get('sign'),
                image_name=candidate.get('image'),
                defaults={
                    "votes": 0
                },
            )

    def add_polling_stations_data(self):
        for polling_station in POLLING_STATIONS:
            PollingStation.objects.get_or_create(
                name=polling_station.get('number'),
                defaults={
                    "total_votes": 0
                },
            )

    def get(self, request):
        self.add_candidate_data()
        self.add_polling_stations_data()
        return redirect("/candidates")


class CandidatesView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'all_candidates.html'

    def get(self, request):
        candidates = []
        lion_votes = 0
        total_votes = 0
        candidates_queryset = Candidate.objects.all().order_by('-votes')
        if candidates_queryset.exists():
            lion_votes = get_lion_votes_string(
                Candidate.objects.get(sign='lion.png').votes,
                candidates_queryset[0].votes,
                candidates_queryset[1].votes
            )
            candidates = []
            for candidate in candidates_queryset:
                total_votes = total_votes + candidate.votes
                if candidate.sign != "lion.png":
                    candidates.append(
                        Candidate(
                            name=get_urdu_candidate_name(candidate.name),
                            sign=candidate.sign,
                            image_name=candidate.image_name,
                            votes=candidate.votes
                        )
                    )
        return Response(
            {
                'candidates': candidates,
                'lion_votes': lion_votes,
                'total_votes': total_votes,
            }
        )


class AddVotesView(View):
    template = 'add_votes.html'

    def get_context(self, is_success=False):
        return {
            "form": PollingStationVoteForm(initial={
                'lion': 0,
                'bat': 0,
                'arrow': 0,
                'rabbit': 0,
                'cup': 0,
                'bowl': 0,
                'crane': 0,
            }),
            "is_success": is_success
        }

    def _create_obj_for_voting(self, ps, candidate_identifier, votes):
        sign = "{}.png".format(candidate_identifier)
        candidate = Candidate.objects.get(sign=sign)
        PollingStationVotes.objects.update_or_create(
            candidate=candidate,
            polling_station=ps,
            defaults={
                "votes": votes
            },
        )

    def _update_polling_station_votes(self, ps, data):
        votes = int(data.get('lion')) + int(data.get('bat')) + int(data.get('cup')) + int(data.get('bowl'))
        votes = votes + int(data.get('crane')) + int(data.get('arrow')) + int(data.get('rabbit'))
        ps.total_votes = votes
        ps.save()

    def _update_cadidate_vote(self, sign):
        votes = PollingStationVotes.objects.filter(candidate__sign=sign).values_list("votes", flat=True)
        candidate = Candidate.objects.get(sign=sign)
        candidate.votes = sum(votes)
        candidate.save()

    def _update_all_candidates_votes(self, data):
        self._update_cadidate_vote("lion.png")
        self._update_cadidate_vote("bat.png")
        self._update_cadidate_vote("arrow.png")
        self._update_cadidate_vote("rabbit.png")
        self._update_cadidate_vote("bowl.png")
        self._update_cadidate_vote("cup.png")
        self._update_cadidate_vote("crane.png")

    def _insert_data(self, data):
        ps = PollingStation.objects.get(id=data.get('polling_station'))
        self._create_obj_for_voting(ps, 'lion', data.get('lion'))
        self._create_obj_for_voting(ps, 'bat', data.get('bat'))
        self._create_obj_for_voting(ps, 'cup', data.get('cup'))
        self._create_obj_for_voting(ps, 'bowl', data.get('bowl'))
        self._create_obj_for_voting(ps, 'crane', data.get('crane'))
        self._create_obj_for_voting(ps, 'arrow', data.get('arrow'))
        self._create_obj_for_voting(ps, 'rabbit', data.get('rabbit'))
        self._update_polling_station_votes(ps, data)
        self._update_all_candidates_votes(data)


    def get(self, request):
        return render(request, self.template, self.get_context())

    def post(self, request):
        form = PollingStationVoteForm(request.POST)
        context = self.get_context(is_success=True)
        if form.is_valid:
            self._insert_data(request.POST)
            context.update({
                "is_success": True
            })
            return redirect("/candidates")
        return render(request, self.template, context)


class PollingStationView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'polling_stations.html'

    def get(self, request):
        all_polling_stations_votes = 0
        number_of_polling_stations = 0
        all_polling_stations = PollingStation.objects.all().order_by("-modified")
        polling_station_votes_list = list()
        for ps in all_polling_stations:
            ps_list = []
            votes = []
            polling_station_votes = 0
            psvs = PollingStationVotes.objects.filter(polling_station=ps)
            if psvs.exists():
                number_of_polling_stations = number_of_polling_stations + 1
                ps_list.append(get_urdu_polling_station_name(ps.name))

                votes.append(psvs.get(candidate__sign="lion.png").votes)
                votes.append(psvs.get(candidate__sign="bat.png").votes)
                votes.append(psvs.get(candidate__sign="arrow.png").votes)
                votes.append(psvs.get(candidate__sign="rabbit.png").votes)
                votes.append(psvs.get(candidate__sign="bowl.png").votes)
                votes.append(psvs.get(candidate__sign="cup.png").votes)
                votes.append(psvs.get(candidate__sign="crane.png").votes)
                if votes:
                    polling_station_votes = sum(votes)
                max_vote = max(votes)
                for index, vote in enumerate(votes):
                    if max_vote == vote:
                        ps_list.append("{}***".format(str(vote)))
                    else:
                        ps_list.append(str(vote))
                all_polling_stations_votes = all_polling_stations_votes + polling_station_votes
                ps_list.append(polling_station_votes)
                polling_station_votes_list.append(ps_list)

        return Response(
            {
                'total_votes': all_polling_stations_votes,
                'polling_station_count': number_of_polling_stations,
                'polling_station_votes': polling_station_votes_list
            }
        )


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
