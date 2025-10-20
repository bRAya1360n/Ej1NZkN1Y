# 代码生成时间: 2025-10-20 20:50:11
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config
import requests
import logging

# 设置日志记录
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 持续集成工具类
class ContinuousIntegrationTool:
    def __init__(self, base_url, build_url, auth):
        self.base_url = base_url
        self.build_url = build_url
        self.auth = auth

    def trigger_build(self, repository_id, branch):
        """触发构建"""
        try:
            response = requests.post(
                f"{self.base_url}{self.build_url}",
                json={'repository_id': repository_id, 'branch': branch},
                auth=self.auth
            )
            response.raise_for_status()
            return {'status': 'success', 'message': 'Build triggered successfully'}
        except requests.RequestException as e:
            logger.error(f'Failed to trigger build: {e}')
            return {'status': 'error', 'message': 'Failed to trigger build'}

# Pyramid视图函数
@view_config(route_name='trigger_build', request_method='POST', renderer='json')
def trigger_build_view(request):
    repo_id = request.json.get('repository_id')
    branch = request.json.get('branch')
    if not repo_id or not branch:
        return Response(json_body={'status': 'error', 'message': 'Repository ID and branch are required'},
                       content_type='application/json', status=400)
    
    # 这里填写CI工具的基本信息
    ci_tool = ContinuousIntegrationTool(
        base_url='https://ci.example.com/api',
        build_url='/build',
        auth=('user', 'password')
    )
    
    result = ci_tool.trigger_build(repo_id, branch)
    return Response(json_body=result, content_type='application/json')

# Pyramid配置函数
def main(global_config, **settings):
    """Assuming 'settings' is a dict with your custom settings."""
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.add_route('trigger_build', '/trigger_build')
    config.scan()
    return config.make_wsgi_app()
