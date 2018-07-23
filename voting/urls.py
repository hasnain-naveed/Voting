"""voting URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url, include
from rest_framework import routers
from core.views import UserViewSet, GroupViewSet, CandidatesView, AddVotesView, PollingStationView, AddDataView
from django.contrib import admin

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include(router.urls)),
    url(r'^candidates', CandidatesView.as_view(), name="candidate"),
    url(r'^add_vote', AddVotesView.as_view(), name="add_vote"),
    url(r'^polling_stations', PollingStationView.as_view(), name="polling_station"),
    url(r'^add_data', AddDataView.as_view(), name="add_data"),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]