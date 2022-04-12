import enum
import random
from model_utils import Choices
from django.utils.translation import gettext as _


@enum.unique
class MessageResponse(enum.Enum):
    TEAM = "Team"
    PLAYER = "Player"

    INDEX_FIRST = 20
    INDEX_SECOND = 15
    INDEX_THIRD = 9
    INDEX_FOURTH = 3

    TYPE_1 = "attacker"
    TYPE_2 = "midfielder"
    TYPE_3 = "defender"
    TYPE_4 = "goalkeeper"


def create_players(country, team):
    try:
        player_list = []
        type = None
        for index in range(1, 21):
            if index <= MessageResponse.INDEX_FIRST.value:
                type = MessageResponse.TYPE_1.value
            if index <= MessageResponse.INDEX_SECOND.value:
                type = MessageResponse.TYPE_2.value
            if index <= MessageResponse.INDEX_THIRD.value:
                type = MessageResponse.TYPE_3.value
            if index <= MessageResponse.INDEX_FOURTH.value:
                type = MessageResponse.TYPE_4.value

            player_data = {
                "first_name": "Player " + str(index) + " First Name",
                "last_name": "Player " + str(index) + " Last Name",
                "country": country,
                "player_type": type,
                "age": random.randint(18, 40),
                "team": team,
            }
            player_list.append(player_data)
        return player_list
    except Exception as e:
        raise e


STATUS = Choices(
    # here are the statuses of user transfer
    ("New", _("New")),
    ("Transferred", _("Transferred")),
)