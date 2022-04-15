from django.test import TestCase
from django.contrib.auth.models import User
from api.models import (
    Team,
    Player,
    TransferList
)


class PlayerModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        user = User.objects.create_user(
            "test_username",
            "test@email.com",
            "12345678@"
        )
        team = Team.objects.create(user=user, team_name='Test Team')
        Player.objects.create(
            first_name='Test First Name',
            last_name="Test Last Name",
            country="Test Country",
            player_type="Test Type",
            team=team
        )

    def test_team_name_label(self):
        team = Team.objects.get(id=1)
        field_label = team._meta.get_field('team_name').verbose_name
        self.assertEqual(field_label, 'Team Name')

    def test_team_name_max_length(self):
        team = Team.objects.get(id=1)
        max_length = team._meta.get_field('team_name').max_length
        self.assertEqual(max_length, 30)

    def test_team_name_not_max_length(self):
        team = Team.objects.get(id=1)
        max_length = team._meta.get_field('team_name').max_length
        self.assertNotEqual(max_length, 100)

    def test_team_country_label(self):
        team = Team.objects.get(id=1)
        field_label = team._meta.get_field('team_country').verbose_name
        self.assertEqual(field_label, 'Team Country')

    def test_team_country_max_length(self):
        team = Team.objects.get(id=1)
        max_length = team._meta.get_field('team_country').max_length
        self.assertEqual(max_length, 30)

    def test_team_country_not_max_length(self):
        team = Team.objects.get(id=1)
        max_length = team._meta.get_field('team_country').max_length
        self.assertNotEqual(max_length, 100)

    def test_first_name_label(self):
        player = Player.objects.get(id=1)
        field_label = player._meta.get_field('first_name').verbose_name
        self.assertEqual(field_label, 'First Name')

    def test_first_name_max_length(self):
        player = Player.objects.get(id=1)
        max_length = player._meta.get_field('first_name').max_length
        self.assertEqual(max_length, 30)

    def test_first_name_not_max_length(self):
        player = Player.objects.get(id=1)
        max_length = player._meta.get_field('first_name').max_length
        self.assertNotEqual(max_length, 100)

    def test_last_name_label(self):
        player = Player.objects.get(id=1)
        field_label = player._meta.get_field('last_name').verbose_name
        self.assertEqual(field_label, 'Last Name')

    def test_last_name_max_length(self):
        player = Player.objects.get(id=1)
        max_length = player._meta.get_field('last_name').max_length
        self.assertEqual(max_length, 30)

    def test_last_name_not_max_length(self):
        player = Player.objects.get(id=1)
        max_length = player._meta.get_field('last_name').max_length
        self.assertNotEqual(max_length, 100)

    def test_country_label(self):
        player = Player.objects.get(id=1)
        field_label = player._meta.get_field('country').verbose_name
        self.assertEqual(field_label, 'Country Name')

    def test_country_max_length(self):
        player = Player.objects.get(id=1)
        max_length = player._meta.get_field('country').max_length
        self.assertEqual(max_length, 30)

    def test_country_not_max_length(self):
        player = Player.objects.get(id=1)
        max_length = player._meta.get_field('country').max_length
        self.assertNotEqual(max_length, 100)

    def test_player_type_label(self):
        player = Player.objects.get(id=1)
        field_label = player._meta.get_field('player_type').verbose_name
        self.assertEqual(field_label, 'Player Type')

    def test_player_type_max_length(self):
        player = Player.objects.get(id=1)
        max_length = player._meta.get_field('player_type').max_length
        self.assertEqual(max_length, 30)

    def test_player_type_not_max_length(self):
        player = Player.objects.get(id=1)
        max_length = player._meta.get_field('player_type').max_length
        self.assertNotEqual(max_length, 100)


class TransferModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        user = User.objects.create_user(
            "test_username",
            "test@email.com",
            "12345678@"
        )
        team = Team.objects.create(user=user, team_name='Test Team')
        player = Player.objects.create(
            first_name='Test First Name',
            last_name="Test Last Name",
            country="Test Country",
            player_type="Test Type",
            team=team
        )
        TransferList.objects.create(
            user=user,
            player=player,
            asking_price=75,
        )

    def test_asking_price_max_digits(self):
        transfer_list = TransferList.objects.get(id=1)
        field_label = transfer_list._meta.get_field('asking_price').max_digits
        self.assertEqual(field_label, 6)

    def test_asking_price_not_max_digits(self):
        transfer_list = TransferList.objects.get(id=1)
        field_label = transfer_list._meta.get_field('asking_price').max_digits
        self.assertNotEqual(field_label, 10)
