from django.db import models
from django.contrib.auth.models import User
from .managers import PlayersManager, TransferManager
from django.db.models import Sum
from soccer_app.utils import (
    STATUS,
)


class Log_Created(models.Model):
    """ Abstract model containing common fields."""
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Team(Log_Created):
    """
        All Available Team for a specific user
    """
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="teams"
    )
    team_name = models.CharField("Team Name", max_length=30)
    team_country = models.CharField("Team Country", max_length=30)
    team_value = models.DecimalField(default=20.000, decimal_places=3, max_digits=6)
    additional_resource = models.DecimalField(default=5.000, decimal_places=3, max_digits=6)

    class Meta:
        """
            Get Team Default by newly created order
        """
        ordering = ["-created_on"]

        """
            Create Indexing Based on Team Name
        """
        indexes = [
            models.Index(fields=['team_name'], name="team_name_idx")
        ]

    def __str__(self):
        """
            Get team name associated with primary key and Model(Table) Name
        """
        return f"{self.team_name}__{self.pk}_Team"


    @property
    def team_total_value(self):
        query_set = self.players.check_is_transferred()
        return query_set.aggregate(team_value=Sum("market_value"))["team_value"]


    @classmethod
    def create_team(cls, data):
        return cls.objects.create(**data)


    @classmethod
    def update_team_resource(cls, buying_team, updated_budget, selling_team):
        """ Update team resource (budget) whenever a player is bought and sold for bith team """
        buying_team.additional_resource -= updated_budget
        buying_team.save()

        selling_team.additional_resource  += updated_budget
        selling_team.save()


class Player(Log_Created):
    """
        All Available players related with a team
    """
    first_name = models.CharField("First Name", max_length=30)
    last_name = models.CharField("Last Name", max_length=30)
    country = models.CharField("Country Name", max_length=30)
    player_type = models.CharField("Player Type", max_length=30)
    initial_value = models.DecimalField(default=1.000, decimal_places=3, max_digits=6)
    age = models.BigIntegerField(default=0)
    market_value = models.BigIntegerField(default=1)
    team = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name="players"
    )
    is_transferred = models.BooleanField(default=False)

    objects = PlayersManager()

    class Meta:
        """
            Get Players default by newly created order
        """

        ordering = ["-created_on"]

        """
            Create Indexing Based on country
        """

        indexes = [
            models.Index(fields=['country'], name="country__idx")
        ]


    def __str__(self):
        """
            Get players name associated with primary key and Model(Table) Name
        """
        return f"{self.first_name}__{self.last_name}__{self.pk}_Player"


    @classmethod
    def create_player(cls, objs=[]):
        """
            Create new players
        """
        players = [
            cls(
                first_name=obj["first_name"],
                last_name=obj["last_name"],
                country=obj["country"],
                player_type=obj["player_type"],
                age=obj["age"],
                team=obj["team"]
            )
            for obj in objs
            if obj
        ]
        cls.objects.bulk_create(players)

    @classmethod
    def update_transfer(cls, player, value, team, status):
        try:
            player.market_value = value
            player.team = team
            player.is_transferred = status
            player.save()
        except Exception as e:
            raise e


class TransferList(Log_Created):
    """
        All Available players on transfer list
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="transferring_user"
    )
    player = models.ForeignKey(
        Player, on_delete=models.CASCADE, related_name="transfers"
    )
    asking_price =models.DecimalField(max_digits=6, decimal_places=2)
    status = models.CharField(choices=STATUS, default=STATUS.New, max_length=12)


    class Meta:
        """
            Get List Default by newly created order
        """
        ordering = ["-created_on"]

        """
            Create Indexing Based on player
        """
        indexes = [
            models.Index(fields=['player'], name="player_idx")
        ]

    def __str__(self):
        """
            Get user associated with primary key and Model(Table) Name
        """
        return f"{self.user}__{self.pk}_TransferList"

    objects = TransferManager()

    @property
    def team(self):
        return f"{self.player.team.team_name}"

    @property
    def country(self):
        return f"{self.player.country}"

    @property
    def player_name(self):
        return f"{self.player.first_name}" ' ' f"{self.player.last_name}"

    @property
    def player_value(self):
        return f"{self.player.market_value}"

    @classmethod
    def transfer_status(cls, list_player, status):
        list_player.status = status
        list_player.save()
