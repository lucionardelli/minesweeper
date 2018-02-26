from rest_framework import serializers

from minesweeper.apps.game.models import Game


class GameSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Game
        fields = ['id',
            'url',
            'name',
            'user',
            'create_date',
            'finish_date',
            'last_action',
            'elapsed_time',
            'status',
            'rows',
            'columns',
            'mines'
        ]
        read_only_fields = ['id', 'user', 'create_date', 'finish_date', 'last_action', 'elapsed_time', 'status', 'url']


    def get_url(self, obj):
        request = self.context.get("request")
        return obj.get_api_url(request=request)

    def validate_name(self, value):
        qs = Game.objects.filter(name=value)
        if self.instance:
            qs = qs.exclude(id=self.instance.id)
        if qs.exists():
            raise serializers.ValidationError("Some other game has this name!")
        return value

