from django.contrib import admin
from api.models import (
    Team,
    Player,
    TransferList,
)
# Register your models here.

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "team_name", "team_country", "team_value", "additional_resource",)
    date_hierarchy = 'created_on'


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name", "country", "player_type", "initial_value", "age", "market_value", "team", )
    date_hierarchy = 'created_on'


@admin.register(TransferList)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ("id", "team", "country", "player_name", "player_value", "asking_price",)
    date_hierarchy = 'created_on'