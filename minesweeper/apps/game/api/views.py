from rest_framework import generics, mixins
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.serializers import ValidationError

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
        row = request.data.get('rows')
        col = request.data.get('columns')
        mines = request.data.get('mines')
        if mines >= row + col:
            raise ValidationError("The number if mines should be less than #Rows + #Cols -1!")
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

    def put(self, request, *args, **kwargs):
        """
        API for making a new play on the minesweeper
        game.
        Args:
            row (int): The first parameter.
            col (int): The second parameter.
            sign (char, optional): Defaults to None. Indicates the
                    kind of move intended.
        Returns:
            bool: True if a valid move was made, False otherwise.

        - If sign is None, it indicates that a cell have
          been chosen to be revealed.
        - If sign is 'F', it indicates that the cell (row, col)
          have been flagged.
        - If sign is '?', it indicates that the cell (row, col)
          have been marked witha a question mark.
        - If sign is '' it indicates that the cell (row, col)
          have been cleared of any markings.
        """
        game = self.get_object()
        if game.status == game.PAUSED:
            raise ValidationError("The game is paused!")
        elif game.status in (game.LOST, game.WON):
            raise ValidationError("The game has ended!")
        row = request.data.get('row')
        col = request.data.get('column')
        sign = request.data.get('sign')
        if row is None or col is None or row + 1 > game.rows or col + 1 > game.columns:
            raise ValidationError("The selected cell is not valid!")
        game.make_move(row, col, sign=sign)
        serializer = GameSerializer(game, context={'request': request}, many=False)
        return Response(serializer.data)

