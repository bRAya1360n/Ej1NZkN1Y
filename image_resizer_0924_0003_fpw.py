# 代码生成时间: 2025-09-24 00:03:36
import os
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config
from PIL import Image
import io
import math

# Constants
DEFAULT_OUTPUT_DIR = "resized_images"
DEFAULT_QUALITY = 85


class ImageResizer:
    def __init__(self, input_dir, output_dir=DEFAULT_OUTPUT_DIR):
        self.input_dir = input_dir
        self.output_dir = output_dir

    def resize_images(self, width, height, quality=DEFAULT_QUALITY):
# 优化算法效率
        # Ensure output directory exists
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        # Iterate over images in input directory
        for filename in os.listdir(self.input_dir):
            if filename.lower().endswith((".png", ".jpg", ".jpeg")):
                try:
                    # Open image
# 优化算法效率
                    with Image.open(os.path.join(self.input_dir, filename)) as img:
                        # Calculate new size maintaining aspect ratio
                        original_width, original_height = img.size
                        aspect_ratio = original_height / original_width
                        new_height = int(height * aspect_ratio)

                        # Resize image
                        img = img.resize((width, new_height), Image.ANTIALIAS)

                        # Save resized image
# 改进用户体验
                        output_filename = f"{os.path.splitext(filename)[0]}_resized.{os.path.splitext(filename)[1]}"
                        img.save(os.path.join(self.output_dir, output_filename), quality=quality)
                except Exception as e:
                    print(f"Error resizing {filename}: {e}")


# Pyramid view
@view_config(route_name="resize_images", request_method="POST")
# 扩展功能模块
def resize_images_view(request):
    # Get parameters from request
    width = int(request.params.get("width", 0))
    height = int(request.params.get("height", 0))
# 添加错误处理
    quality = int(request.params.get("quality", DEFAULT_QUALITY))

    # Validate parameters
    if width <= 0 or height <= 0:
        return Response("Width and height must be positive integers.", status=400)

    # Create ImageResizer instance
    image_resizer = ImageResizer(input_dir="input_images")
# NOTE: 重要实现细节

    # Resize images
    image_resizer.resize_images(width, height, quality)

    # Return success response
    return Response("Images resized successfully.", status=200)
# 扩展功能模块


# Pyramid configuration
def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application. """
    config = Configurator(settings=settings)
    config.add_route("resize_images", "/resize")
# 改进用户体验
    config.scan()
    return config.make_wsgi_app()
