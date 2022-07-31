from display.models.image import Image
from display.serializers.displayserializers import DisplayAllSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from util.functions.utilfunctions import get_uid
from display.serializers.imageserializers import ImageAllSerializer, ImagePathSerializer
from display.models import Display


class DisplayView(APIView):
    """
    View for returning and updating a display
    """

    def get(self, request):
        """
        Request Type: GET
        Returns news for current user
        """
        display = Display.objects.get(uid=get_uid(request))
        serializer = ImagePathSerializer(display.image)

        return Response(serializer.data, status=status.HTTP_200_OK)


    def put(self, request):
        """
        Expected PUT Data:
        {
            "image": optional | {"file": b64, "file_path": str}
        }
        """

        display = Display.objects.get(uid=get_uid(request))

        if (photo := request.data['image']) is not None:
            file_path = f'/images/{display.id}/{photo["file_path"]}'
            # Update image
            if display.image is not None:
                queried_photo = Image.objects.get(display=display)
                queried_photo.update_s3_repo(photo['file'], file_path)
            # Create image
            else:
                file_serializer = ImageAllSerializer(data={**photo, 'file_path': file_path}, context=photo['file'])
                file_serializer.is_valid(raise_exception=ValueError)
                created_file = file_serializer.save()

                display.image = created_file
                display.save()

        serializer = DisplayAllSerializer(display)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        NOTE: Only used for testing
        Expected Post Data:
        {
            uid: str
            phone_number: str
            image: optional image object
        }
        """
        
        display_data = request.data

        serializer = DisplayAllSerializer(data=display_data)
        serializer.is_valid(raise_exception=ValueError)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
