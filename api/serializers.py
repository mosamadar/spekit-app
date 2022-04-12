from rest_framework import serializers
from rest_framework_friendly_errors.mixins import FriendlyErrorMessagesMixin
from api.models import (
    Team,
    Player,
    TransferList,
)
from django.db import transaction
import random
from soccer_app.utils import create_players


class TeamSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    """
        Get the user team and all players of team
    """
    all_players = serializers.SerializerMethodField()

    @staticmethod
    def get_all_players(self):
        queryset = self.players.check_is_transferred()
        serializer = PlayerSerializer(queryset, many=True)
        return serializer.data

    class Meta:
        model = Team
        fields = (
            "id",
            "team_name",
            "team_country",
            "team_total_value",
            "additional_resource",
            "all_players",
        )

    def create(self, validated_data):
        user = self.context.get('user')
        team_name = validated_data.get('team_name')
        country = validated_data.get('team_country')

        data = {
            "user": user,
            "team_name": team_name,
            "team_country": country,
        }
        with transaction.atomic():
            team = Team.objects.create(**data)
            players_data = create_players(country, team)
            Player.create_player(players_data)
        return team

    def update(self, instance, validated_data):
        """
            Update a single team details
        """
        instance.team_name = validated_data.get("team_name", instance.team_name)
        instance.team_country = validated_data.get("team_country", instance.team_country)
        instance.save()
        return instance


class PlayerSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    """
        Get the user players associated with the team
    """
    class Meta:
        model = Player
        fields = (
            "id",
            "first_name",
            "last_name",
            "country",
            "player_type",
            "age",
            "market_value"
        )

    def update(self, instance, validated_data):
        """
            Update a single player of a team
        """
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.country = validated_data.get("country", instance.country)
        instance.save()
        return instance


class TransferPlayerSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    """
        Get the transfer list of all players by all users
    """
    class Meta:
        model = TransferList
        fields = [
            "player",
            "asking_price",
        ]

    def create(self, validated_data):
        user = self.context.get('user')
        player = validated_data.get('player')
        asking_price = validated_data.get('asking_price')

        with transaction.atomic():
            """
                Create a new player to be sold on market with 
                adding player details
                eg : asking price 
                player details : (name, team_name , country)
                add specific player transfer boolean to set 
                and show in market
            """
            Player.update_transfer(
                player, player.market_value, user.teams, True
            )
            data = {
                    "user": user,
                    "player": player,
                    "asking_price": asking_price,
            }
            transfer = TransferList.objects.create(**data)
        return transfer


class PlayerTransferListSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    """
        Get the transfer list of all players by all users
    """
    class Meta:
        model = TransferList
        fields = (
            "id",
            "player_id",
            "team",
            "country",
            "player_name",
            "player_value",
            "asking_price",
            "status",
        )


class BuyPlayerSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    """
        Buy the player from transfer list of all players by all users
    """
    class Meta:
        model = TransferList
        fields = [
            "player",
            "asking_price",
        ]

    def create(self, validated_data):
        user = self.context.get('user')
        player = validated_data.get('player')
        asking_price = validated_data.get('asking_price')

        """
            Check if current buying team budget is greater than asking price
        """
        if user.teams.additional_resource > asking_price:
            with transaction.atomic():
                """
                    Add random player market_value based on value
                """
                player_value = random.randint(10, 100)
                """
                    Update Buying(Decrease) and Selling(Increase) 
                    team resource(Budget) based on requirements
                """
                Team.update_team_resource(
                    user.teams, asking_price, player.team
                )
                """
                   Set selling player transfer status to false 
                   to remove from market after biding or purchase 
                   order is done and (Set a player value and New Team)
                   to which the player is sold to.
                """
                Player.update_transfer(
                    player, player_value, user.teams, False
                )
                """
                   Set transfer list status from open(New) to
                   (Transferred) closed.
                """
                try:
                    get_list_id = TransferList.objects.get(player=player)
                    TransferList.transfer_status(get_list_id, "Transferred")
                except Exception as e:
                    raise e
            return get_list_id
        else:
            return False


class AdminPlayerSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = [
            "first_name",
            "last_name",
            "country",
            "player_type",
            "team",
        ]

    def create(self, validated_data):
        return Player.objects.create(**validated_data)


    def update(self, instance, validated_data):
        """
            Admin update any player of the system
        """
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.country = validated_data.get("country", instance.country)
        instance.initial_value = validated_data.get("initial_value", instance.initial_value)
        instance.market_value = validated_data.get("market_value", instance.market_value)
        instance.save()
        return instance
