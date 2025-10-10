# 代码生成时间: 2025-10-10 19:35:06
# digital_watermarking.py

"""
A Pyramid application that demonstrates the implementation of digital watermarking technology.
This program embeds a watermark into an image, allowing for the detection of unauthorized copying or modifications.
"""

from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config
from PIL import Image
import numpy as np
import io
import base64
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

# Constants
DEFAULT_WATERMARK_TEXT = "Secret Watermark"
def apply_watermark(input_image_path, watermark_text=DEFAULT_WATERMARK_TEXT):
    """
    Applies a watermark to the given image.

    :param input_image_path: Path to the input image.
    :param watermark_text: Text to be used as the watermark.
    :return: A PIL Image object with the watermark applied.
    """
    try:
        # Load the input image
        image = Image.open(input_image_path)
        # Convert the image to a numpy array for manipulation
        image_array = np.array(image)
        
        # Define the position for the watermark
        watermark_position = (10, 10)
        
        # Convert the watermark text to a numpy array
        watermark_array = np.array(Image.fromarray(np.zeros((100, 100, 3), dtype=np.uint8))
                                      .putalpha(Image.new('L', (100, 100)).textsize(watermark_text, font=Image.font.load_default())))
        
        # Embed the watermark into the image
        image_array[watermark_position[1]:watermark_position[1]+100,
                   watermark_position[0]:watermark_position[0]+100, :] = watermark_array
        
        # Convert the numpy array back to a PIL Image object
        watermarked_image = Image.fromarray(image_array)
        
        return watermarked_image
    except Exception as e:
        log.error(f"An error occurred while applying the watermark: {e}")
        raise


def remove_watermark(image_path):
    """
    Removes the watermark from the given image, if possible.

    :param image_path: Path to the image with the watermark.
    :return: A PIL Image object with the watermark removed.
    """
    try:
        # Load the image with the watermark
        image = Image.open(image_path)
        # Convert the image to a numpy array for manipulation
        image_array = np.array(image)
        
        # Define the position for the watermark
        watermark_position = (10, 10)
        
        # Remove the watermark by setting the area to original image's color
        original_color = image_array[watermark_position[1]+1, watermark_position[0]+1]
        image_array[watermark_position[1]:watermark_position[1]+100,
                   watermark_position[0]:watermark_position[0]+100, :] = original_color
        
        # Convert the numpy array back to a PIL Image object
        non_watermarked_image = Image.fromarray(image_array)
        
        return non_watermarked_image
    except Exception as e:
        log.error(f"An error occurred while removing the watermark: {e}")
        raise

# Pyramid view
@view_config(route_name='watermark', renderer='json')
def watermark_view(request):
    "