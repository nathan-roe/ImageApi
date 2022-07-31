from django.db import models
from django.utils.functional import cached_property

from file_storage.functions import delete_file, upload_file

from util.functions.imagefunctions import b64_to_fileobj


class File(models.Model):
    """
    Model reduces logic in other models and allows model relationships
    """

    class Meta:
        abstract = True
    # NOTE: Currently only saving cropped image file
    file_path = models.CharField(max_length=255, null=True, blank=True)

    # S3 url for front end use
    @cached_property
    def file_url(self):
        """Returns the S3 file"""
        from util.functions.imagefunctions import get_file_url
        return get_file_url(self.file_path)
    
    # updates an existing file
    def update_s3_repo(self, file, new_file_path):
        """
        Updates a file in s3 and saves the model accordingly
        """
        # update file
        if file:
            delete_file(self.file_path)
            upload_file(new_file_path, b64_to_fileobj(file))
            self.file_path = new_file_path
            self.save()
        # self destruct
        else:
            self.delete()

    # deletes file in S3 when the model is deleted
    def delete(self, *args, **kwargs):
        """
        Method used to remove S3 file from AWS before deletion
        """
        delete_file(self.file_path)
        super().delete(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.file_path} | ID: {self.id}'


class Image(File):
    pass
