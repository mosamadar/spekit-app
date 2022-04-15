from rest_framework_simplejwt.tokens import RefreshToken
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from api.models import (
    Team,
    Player,
    TransferList
)
import random

class TeamListViewTest(TestCase):
    def bearer_token(self):
        # assuming there is a user in User model
        user = User.objects.create_user(
            f"username.test_{random.randint(1, 1000)}",
            f"test_{random.randint(1, 1000)}@email.com",
            "12345678@"
        )
        refresh = RefreshToken.for_user(user)
        return {"HTTP_AUTHORIZATION": f'Bearer {refresh.access_token}'}

    @classmethod
    def setUpTestData(cls):
        # Create 12 teams for test_api
        number_of_teams = 12
        for index in range(1, number_of_teams):
            user = User.objects.create_user(
                f"username.{index}",
                f"test_{index}@email.com",
                "12345678@"
            )
            Team.objects.create(
                user=user,
                team_name=f'Team {index}',
            )

    def test_view_url_not_exists_at_desired_location(self):
        self.client.login(email='test_1@email.com', password='12345678@')
        response = self.client.get('/api/team/')
        self.assertEqual(response.status_code, 401)

    def test_view_url_not_accessible_by_name(self):
        self.client.login(email='test_1@email.com', password='12345678@')
        response = self.client.get(reverse('get_teams'))
        self.assertEqual(response.status_code, 401)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/api/team/', self.bearer_token)
        self.assertEqual(response.status_code, 200)


class PlyerListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create 12 players for test_api
        number_of_players = 13
        user = User.objects.create_user(
            "username",
            "test1@email.com",
            "12345678"
        )
        team = Team.objects.create(user=user, team_name='Test Team Two')
        for player_id in range(1, number_of_players):
            Player.objects.create(
                first_name=f'Test First Name {player_id}',
                last_name=f"Test Last Name {player_id}",
                country=f"Test Country {player_id}",
                player_type=f"Test Type {player_id}",
                team=team
            )

    def test_view_url_not_exists_at_desired_location(self):
        response = self.client.get('/api/player/')
        self.assertEqual(response.status_code, 401)

    def test_view_url_not_accessible_by_name(self):
        response = self.client.get(reverse('get_player'))
        self.assertEqual(response.status_code, 401)


class TopicListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create 12 listing for market players
        number_of_transfers = 13
        user = User.objects.create_user(
            "test2_username",
            "test2@email.com",
            "123456789"
        )
        team = Team.objects.create(user=user, team_name='Test Team 2')
        for index in range(1, number_of_transfers):
            player = Player.objects.create(
                first_name=f'Test First Name {index}',
                last_name=f"Test Last Name {index}",
                country=f"Test Country {index}",
                player_type=f"Test Type {index}",
                team=team
            )
            TransferList.objects.create(
                user=user,
                player=player,
                asking_price=index,
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/api/transfer-player/')
        self.assertEqual(response.status_code, 401)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('transfer_player'))
        self.assertEqual(response.status_code, 401)

    def test_find_document(self):
        # Get documents by desired params
        response = self.client.get(reverse('transfer_list') + '?country=Test Country 2&team_name=Test Team 2&value=1')
        self.assertEqual(response.status_code, 401)
        # self.assertEqual(len(response.context['document_list']), 3)