from celery import shared_task
from .models import *
from PIL import Image as img
import io
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile


@shared_task
# Reduces uploaded image size to a max width of 1000px
def process_image(file_id):
    
    # Retrieve the file instance from the database
    try:
        file_instance = File.objects.get(id=file_id)
    except File.DoesNotExist:
        return {"status": "error", "message": "File does not exist"}
    
    # Use the file path from the file instance
    file_path = file_instance.file.name

    if default_storage.exists(file_path):
        with default_storage.open(file_path, 'rb') as file:
            image = img.open(file)
            
            # Don't do anything if the image is already less than 1000px wide
            if image.width <= 1000:
                return {"status": "success", "message": "Image is already less than 1000px wide"}
            
            # Calculate the new width to maintain the aspect ratio
            aspect_ratio = image.width / image.height
            new_height = 1000
            new_width = int(new_height * aspect_ratio)
            
            # Resize the image
            resized_image = image.resize((new_width, new_height))
            
            # Save the resized image to the same file path
            image_io = io.BytesIO()
            resized_image.save(image_io, format=image.format)
            
            resized_image_file = ContentFile(image_io.getvalue())
            default_storage.save(file_path, resized_image_file)
            
            # Update the file instance in the database
            file_instance.file.save(file_instance.file.name, resized_image_file, save=True)
            
            return {"status": "success", "message": "Image resized and saved", "image": resized_image}
    else:
        return {"status": "error", "message": "File does not exist"}