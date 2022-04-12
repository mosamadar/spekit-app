from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from api.models import Team, Player
from django.db import transaction
from soccer_app.utils import MessageResponse, create_players


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    username = serializers.CharField(
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    password = serializers.CharField(min_length=8, write_only=True)
    country = serializers.CharField(required=True)


    def create(self, validated_data):
        username = validated_data.get('username')
        email = validated_data.get('email')
        password = validated_data.get('password')
        country = validated_data.get('country')

        with transaction.atomic():
            user = User.objects.create_user(
                username,
                email,
                password
            )
            team_data = {
                "user": user,
                "team_name": str(username + " " + MessageResponse.TEAM.value),
                "team_country": country
            }
            team = Team.create_team(team_data)
            players_data = create_players(country, team)
            Player.create_player(players_data)
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'country')
