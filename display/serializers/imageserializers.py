from rest_framework import serializers
from util.functions.imagefunctions import upload_file
from util.functions.utilfunctions import b64_to_fileobj
from display.models import Image


class FileSerializerMixin(metaclass=serializers.SerializerMetaclass):
    """
    Mixin used for create and update functionality
    """
    def create(self, cleaned_data):
        file = self.context
        if file is None:
            raise ValueError("Context is required")
        upload_file(cleaned_data["file_path"], b64_to_fileobj(file))
        return self.Meta.model.objects.create(**cleaned_data)

    def update(self, instance, validated_data):
        if (file := self.context) is not None and 'file_path' in validated_data:
            instance.update_s3_repo(file, validated_data['file_path'])
        return super().update(instance, validated_data)


class ImageAllSerializer(FileSerializerMixin, serializers.ModelSerializer):
    """
    Serializer for handling Image objects with all fields returned
    """
    class Meta:
        model = Image
        fields = '__all__'


class ImagePathSerializer(serializers.ModelSerializer):
    """
    Serializer to return Image path
    """
    class Meta:
        model = Image
        fields = ['id', 'file_url']
