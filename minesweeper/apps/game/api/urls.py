from django.conf.urls import url

from .views import GameDetailView, GameAPIView

app_name = 'minesweeper'

urlpatterns = [
    url(r'^$', GameAPIView.as_view(), name='game-list-and-create'),
    url(r'^(?P<id>\d+)/$', GameDetailView.as_view(), name='game-detail')
]
