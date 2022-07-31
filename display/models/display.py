from django.db import models
from image import Image

class Display(models.Model):
    uid = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=50)
    image = models.OneToOneField(Image, related_name='display', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'uid: {self.uid} | phone_number: {self.phone_number} | Display: {self.image} | ID: {self.id}'
