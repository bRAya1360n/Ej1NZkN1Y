# 代码生成时间: 2025-11-03 01:10:03
import os
from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPInternalServerError, HTTPBadRequest
from PIL import Image
import pytesseract

# 配置PyTesseract路径
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'  # Windows系统的路径


def get_ocr_text(image_path):
    """
    使用OCR技术识别图片中的文字。
    
    参数:
        image_path (str): 图片文件的路径。
    
    返回:
        str: 图片中识别到的文字。
    """
    try:
        # 打开图片文件
        img = Image.open(image_path)
        # 使用pytesseract进行文字识别
        text = pytesseract.image_to_string(img)
        return text
    except Exception as e:
        # 错误处理
        raise HTTPInternalServerError(body=str(e))

@view_config(route_name='ocr', renderer='json')
def ocr_view(request):
    """
    Pyramid视图函数，处理OCR识别请求。
    
    参数:
        request (Request): Pyramid的请求对象。
    
    返回:
        Response: 返回包含识别文字的JSON响应。
    """
    try:
        # 获取请求参数
        image_path = request.matchdict['image_path']
        # 检查图片路径
        if not os.path.isfile(image_path):
            return HTTPBadRequest('Image path does not exist.')
        # 调用OCR函数
        ocr_text = get_ocr_text(image_path)
        return {'ocr_result': ocr_text}
    except HTTPBadRequest as e:
        return e
    except Exception as e:
        return HTTPInternalServerError(body=str(e))
