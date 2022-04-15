from api.baseview import BaseAPIView
from .serializers import UserSerializer
from rest_framework import status
from rest_framework.permissions import  IsAdminUser
from .authentication_backend import AdminAuthenticationPermission
from api.models import Team, Player
from api.serializers import (
    TeamSerializer,
    PlayerSerializer,
    AdminPlayerSerializer
)
from django.shortcuts import get_object_or_404
# Create your views here.


class SignUpUser(BaseAPIView):
    """
    Creates the user.
    """
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                return self.send_response(
                    success=True,
                    code=f"201.",
                    status_code=status.HTTP_201_CREATED,
                    payload="",
                    description="User created successfully.",
                )
        return self.send_response(
            success=False,
            payload={},
            description=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST,
        )


class AdminTeamsManagement(BaseAPIView):
    queryset = Team
    serializer_class = TeamSerializer
    permission_classes = (IsAdminUser, AdminAuthenticationPermission, )

    def get(self, request, pk=None):
        """
            Super-admin api view to get all teams of the system
        """
        teams = self.queryset.objects.all()
        serializer = self.serializer_class(teams, many=True)

        return self.send_response(
            success=True,
            payload=serializer.data,
            description="All user teams.",
            status_code=status.HTTP_200_OK,
        )

    def post(self, request):
        """
        Creates a new team by the super-admin.
        :param request:
        :return:
        """
        user = request.user
        data = request.data
        user = None if user.is_anonymous else user
        serializer = self.serializer_class(data=data, context={'request': request, 'user': user})
        if serializer.is_valid():
            serializer.save()
            return self.send_response(
                success=True,
                code=f'201',
                status_code=status.HTTP_201_CREATED,
                payload="",
                description=f'Admin team created successfully.'
            )
        else:
            return self.send_response(
                code=f'422',
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                description='Error occurs while processing',
                exceptions=serializer.errors
            )


    def put(self, request, pk=None):
        """
            Update the team based on team id by admin
        """
        data = request.data
        team_instance = get_object_or_404(self.queryset.objects.all(), pk=pk)
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


    def delete(self, request, pk=None):
        """
            Delete a team based on team id by admin
        """
        if pk:
            team_instance = self.queryset.objects.filter(id=pk)
            team_instance.delete()
            description = 'Team removed successfully'
            return self.send_response(
                success=True,
                payload='',
                description=description,
                status_code=status.HTTP_200_OK
            )
        return self.send_response(
            code=f"422.",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            description="Error occur while processing",
            exceptions="",
        )


class AdminPlayerManagement(BaseAPIView):
    queryset = Player
    serializer_class = PlayerSerializer
    permission_classes = (IsAdminUser, AdminAuthenticationPermission,)

    def get(self, request, pk=None):
        """
            Super-admin api view to get all player of all the teams
        """
        players = self.queryset.objects.all()
        serializer = self.serializer_class(players, many=True)

        return self.send_response(
            success=True,
            payload=serializer.data,
            description="All user teams & players.",
            status_code=status.HTTP_200_OK,
        )

    def post(self, request):
        """
        Creates a new player for a specifci team
        :param request:
        :return:
        """
        user = request.user
        data = request.data
        user = None if user.is_anonymous else user
        serializer = AdminPlayerSerializer(data=data, context={'request': request, 'user': user})
        if serializer.is_valid():
            serializer.save()
            return self.send_response(
                success=True,
                code=f'201',
                status_code=status.HTTP_201_CREATED,
                payload="",
                description=f'Admin team player created successfully.'
            )
        else:
            return self.send_response(
                code=f'422',
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                description='Error occurs while processing',
                exceptions=serializer.errors
            )

    def put(self, request, pk=None):
        """
            Update the team player based on player id by admin
        """
        data = request.data
        player_instance = get_object_or_404(self.queryset.objects.all(), pk=pk)
        serializer = AdminPlayerSerializer(player_instance, data=data, partial=True)
        if serializer.is_valid():
            validated_date = serializer.validated_data
            validated_date["initial_value"] = data.get("initial_value", "")
            validated_date["market_value"] = data.get("market_value", 0)
            instance = serializer.save()
            _player = self.serializer_class(instance).data
            return self.send_response(
                success=True,
                code=f"200.",
                status_code=status.HTTP_200_OK,
                payload=_player,
                description=f"Team player updated successfully",
            )
        else:
            return self.send_response(
                code=f"422.",
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                description="Error occur while processing",
                exceptions=serializer.errors,
            )

    def delete(self, request, pk=None):
        """
            Delete a team player based on player id by admin
        """
        if pk:
            player_instance = self.queryset.objects.filter(id=pk)
            player_instance.delete()
            description = 'Team player removed successfully'
            return self.send_response(
                success=True,
                payload='',
                description=description,
                status_code=status.HTTP_200_OK
            )
        return self.send_response(
            code=f"422.",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            description="Error occur while processing",
            exceptions="",
        )
