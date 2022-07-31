from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from util.functions.utilfunctions import token_to_uid



class DisplayView(APIView):
    """
    View for getting all News
    """
    # authentication_classes = [TokenAuthentication]

    def get(self, request):
        """
        Request Type: GET
        Returns news for current user
        """
        cur_user = token_to_uid(request)

        

        # serializer = NewsListSerializer(query_set, many=True)

        return Response(serializer.data)

