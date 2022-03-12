from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.status import is_server_error
from rest_framework.views import APIView


class BaseAPIView(APIView):
    """
    Base class for API views.
    """
    # authentication_classes = ()
    #permission_classes = []

    def send_response(
        self,
        success=False,
        code="",
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        payload={},
        description="",
        exceptions={},
    ):
        """
        Generates response.
        :param success: bool tells if call is successful or not.
        :param code: str status code.
        :param status_code: int HTTP status code.
        :param payload: list data generated for respective API call.
        :param description: str description.
        :param exception: str description.
        :rtype: dict.
        """
        if not success and is_server_error(status_code):
            if settings.DEBUG:
                description = f"error message: {description}"
            else:
                description = "Internal server error."
        return Response(
            data={
                "success": success,
                "code": code,
                "payload": payload,
                "description": description,
                "exceptions": exceptions,
            },
            status=status_code,
        )

    def send_data_response(
        self,
        success=False,
        code="",
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        payload={},
        description="",
        exceptions={},
    ):
        """
        Generates response for data tables.
        :param success: bool tells if call is successful or not.
        :param code: str status code.
        :param status_code: int HTTP status code.
        :param payload: list data generated for respective API call.
        :param description: str description.
        :rtype: dict.
        """
        if not success and is_server_error(status_code):
            if settings.DEBUG:
                description = f"error message: {description}"
            else:
                description = "Internal server error."
        return Response(
            data={
                "data": {
                    "success": success,
                    "code": code,
                    "payload": payload,
                    "description": description,
                    "exceptions": exceptions,
                }
            },
            status=status_code,
        )
