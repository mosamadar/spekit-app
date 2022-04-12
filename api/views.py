from api.models import (
    Team,
    Player,
    TransferList,
)
from rest_framework import status
from api.serializers import (
    TeamSerializer,
    PlayerSerializer,
    TransferPlayerSerializer,
    PlayerTransferListSerializer,
    BuyPlayerSerializer
)
from api.baseview import BaseAPIView
from django.shortcuts import get_object_or_404
from django.db.models import Q


class TeamApiView(BaseAPIView):
    queryset = Team
    serializer_class = TeamSerializer

    def get(self, request, pk=None):
        """
            Get the team based on user
        """
        user = request.user
        teams = self.queryset.objects.get(user=user)
        serializer = self.serializer_class(teams)

        return self.send_response(
            success=True,
            payload=serializer.data,
            description="User Team",
            status_code=status.HTTP_200_OK,
        )


    def put(self, request, pk=None):
        """
            Update the team based on team id
        """
        user = request.user
        data = request.data
        team_instance = get_object_or_404(self.queryset.objects.filter(user=user), pk=pk)
        serializer = self.serializer_class(team_instance, data=data, partial=True)
        if serializer.is_valid():
            instance = serializer.save()
            _team = self.serializer_class(instance).data
            return self.send_response(
                success=True,
                code=f"200.",
                status_code=status.HTTP_200_OK,
                payload=_team,
                description=f"Team updated successfully",
            )
        else:
            return self.send_response(
                code=f"422.",
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                description="Error occur while processing",
                exceptions=serializer.errors,
            )


class PlayerApiView(BaseAPIView):
    queryset = Player
    serializer_class = PlayerSerializer

    def get(self, request, pk=None):
        """
            Get all the players based on user
        """
        user = request.user
        players = self.queryset.objects.check_is_transferred().filter(team__user=user)
        serializer = self.serializer_class(players, many=True)

        return self.send_response(
            success=True,
            payload=serializer.data,
            description="Total Players",
            status_code=status.HTTP_200_OK,
        )

    def put(self, request, pk=None):
        """
            Update the player based on player id
        """
        user = request.user
        data = request.data
        player_instance = get_object_or_404(self.queryset.objects.filter(team__user=user), pk=pk)
        serializer = self.serializer_class(player_instance, data=data, partial=True)
        if serializer.is_valid():
            instance = serializer.save()
            _player = self.serializer_class(instance).data
            return self.send_response(
                success=True,
                code=f"200.",
                status_code=status.HTTP_200_OK,
                payload=_player,
                description=f"Player updated successfully",
            )
        else:
            return self.send_response(
                code=f"422.",
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                description="Error occur while processing",
                exceptions=serializer.errors,
            )


class TransferPlayer(BaseAPIView):
    queryset = TransferList
    serializer_class = TransferPlayerSerializer
    list_serializer_class = PlayerTransferListSerializer

    def get(self, request):
        """
            Get all the Documents or a single document
        """
        user = request.user
        players = self.queryset.objects.filter(user=user)
        serializer = self.list_serializer_class(players, many=True)

        return self.send_response(
            success=True,
            payload=serializer.data,
            description="Your transferred players",
            status_code=status.HTTP_200_OK,
        )


    def post(self, request):
        """
        Creates a new transfer request for a player.
        :param request:
        :return:
        """
        data = request.data
        user = request.user
        user = None if user.is_anonymous else user
        serializer = self.serializer_class(data=data, context={'request': request, 'user': user})
        if serializer.is_valid():
            serializer.save()
            return self.send_response(
                success=True,
                code=f'201',
                status_code=status.HTTP_201_CREATED,
                payload="",
                description=f'Transfer added successfully'
            )
        else:
            return self.send_response(
                code=f'422',
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                description='Error occurs while processing',
                exceptions=serializer.errors
            )


class GetPlayerTransferList(BaseAPIView):
    queryset = TransferList
    serializer = PlayerTransferListSerializer

    def get(self, request):
        """
            Get the user provided params to search the players
        """
        user = None if request.user.is_anonymous else request.user
        limit = int(request.query_params.get("limit", 10))
        offset = int(request.query_params.get("offset", 0))
        player_country = request.query_params.get("country", "")
        team_name = request.query_params.get("team_name", "")
        player_name = request.query_params.get("player_name", "")
        player_value = request.query_params.get("value", "")

        query_object = Q()

        """
            Combine result based on user params
        """
        if player_country:
            query_object &= Q(player__country__icontains=player_country)
        if team_name:
            query_object &= Q(player__team__team_name__icontains=team_name)
        if player_name:
            query_object &= (Q(player__first_name__icontains=player_name) | Q(player__last_name__icontains=player_name))
        if player_value:
            query_object &= Q(player__market_value__icontains=player_value)

        """
            Query Based on newly added auction players
        """
        records = self.queryset.objects.\
                    get_new_transferred()\
                    .filter(query_object).\
                    exclude(user=user).\
                    distinct()

        """
            Get Limited record based on paginated request
        """
        records = records[offset: offset + limit]

        """
            Serialize the data
        """
        serialized_data = self.serializer(
            records, many=True, context={"request": request, "user": user}
        ).data

        total_count = records.count()
        ranged = offset + limit
        payload = {
            "content": serialized_data,
            "total": total_count,
            "from": offset,
            "to": ranged if ranged < total_count else total_count,
        }

        return self.send_response(
            success=True,
            code=f"201.",
            status_code=status.HTTP_201_CREATED,
            payload=payload,
            description="Player transfer list",
        )


class BuyPlayer(BaseAPIView):
    queryset = TransferList
    serializer_class = BuyPlayerSerializer

    def post(self, request):
        """
        Creates a new buy request for a player.
        :param request:
        :return:
        """
        data = request.data
        user = request.user
        user = None if user.is_anonymous else user
        serializer = self.serializer_class(data=data, context={'request': request, 'user': user})
        if serializer.is_valid():
            response = serializer.save()
            if response:
                message = f'Player bought successfully.'
            else:
                message = f'Your team resources are low to buy this player.'
            return self.send_response(
                success=True,
                code=f'201',
                status_code=status.HTTP_201_CREATED,
                payload="",
                description=message
            )
        else:
            return self.send_response(
                code=f'422',
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                description='Error occurs while processing',
                exceptions=serializer.errors
            )
