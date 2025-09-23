# 代码生成时间: 2025-09-23 16:49:39
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config
from pyramid.session import SignedCookieSessionFactory


# 配置密钥，用于签名会话Cookie
SECRET = 'your-secret-key'


# 创建一个配置器
config = Configurator(settings={'pyramid.secret': SECRET})

# 设置视图
@view_config(route_name='set_theme', request_method='POST')
def set_theme(request):
    # 获取主题参数
    theme = request.params.get('theme', 'default')
    # 设置会话中的主题
    request.session['theme'] = theme
    # 返回响应，告知用户主题已更改
    return Response(f'Theme set to {theme}')

# 设置主题上下文变量
@view_config(context='pyramid.exceptions.NotFound')
def not_found(context, request):
    # 获取当前主题
    theme = request.session.get('theme', 'default')
    # 返回带有主题的404响应
    return Response(f'The requested page is not found. Current theme: {theme}', status=404)

# 配置路由
config.add_route('set_theme', '/set_theme')

# 扫描视图函数
config.scan()


# 运行程序
if __name__ == '__main__':
    app = config.make_wsgi_app()
    from wsgiref.simple_server import make_server
    server = make_server('0.0.0.0', 6543, app)
    print('Serving on http://localhost:6543')
    server.serve_forever()
