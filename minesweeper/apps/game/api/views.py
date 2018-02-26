from rest_framework import generics, mixins
from rest_framework.decorators import detail_route

from minesweeper.apps.game.models import Game
from .permissions import IsOwnerOrReadOnly
from .serializers import GameSerializer

class GameAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    lookup_field            = 'id'
    serializer_class        = GameSerializer

    def get_queryset(self):
        qs = Game.objects.all()
        query = self.request.GET.get("q")
        if query is not None:
            qs = qs.filter(name__icontains=query)
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}


class GameDetailView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field        = 'id'
    ordering_fields     = ('create_date', )
    serializer_class    = GameSerializer
    permission_classes  = [IsOwnerOrReadOnly]

    def get_queryset(self):
        return Game.objects.all()

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

    @detail_route(methods=('post',))
    def make_move(self, request, *args, **kwargs):
        """
        API for making a new play on the minesweeper
        game
        """
        pass

