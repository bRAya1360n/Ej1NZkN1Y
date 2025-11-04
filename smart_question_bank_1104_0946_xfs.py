# 代码生成时间: 2025-11-04 09:46:55
from pyramid.config import Configurator
from pyramid.view import view_config
from pyramid.renderers import render_to_response
from pyramid.response import Response
from pyramid.request import Request
from sqlalchemy import create_engine, Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.security import Allow, Everyone, Authenticated
from pyramid.session import SignedCookieSessionFactory

# 数据库配置
DATABASE_URL = 'sqlite:///:memory:'
engine = create_engine(DATABASE_URL)
Base = declarative_base()
Session = sessionmaker(bind=engine)

# 定义数据库模型
class Question(Base):
    __tablename__ = 'questions'
    id = Column(Integer, Sequence('question_id_seq'), primary_key=True)
    title = Column(String(100))
    content = Column(String(2000))

# 初始化数据库
Base.metadata.create_all(engine)

# Pyramid 配置
def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.add_route('home', '/')
    config.add_route('add_question', '/add')
    config.scan()
    return config.make_wsgi_app()

# 安全配置
def authentication_callback(request):
    return request.unauthenticated_userid or request.authenticated_userid

def includeme(config):
    config.set_authentication_policy(AuthTktAuthenticationPolicy('secret'))
    config.set_authorization_policy(ACLAuthorizationPolicy())
    config.set_default_permission(AllowAnonymous)
    config.set_root_factory('.rootFactory')
    config.registry.settings['pyramid.default_permissions'] = (Allow, Authenticated)

# 视图函数
@view_config(route_name='home', renderer='templates/home.pt')
def home_view(request: Request):
    session = Session()
    questions = session.query(Question).all()
    return {'questions': questions}

@view_config(route_name='add_question', renderer='templates/add_question.pt', request_method='POST')
def add_question_view(request: Request):
    try:
        session = Session()
        title = request.params.get('title')
        content = request.params.get('content')
        new_question = Question(title=title, content=content)
        session.add(new_question)
        session.commit()
        return Response('Question added successfully')
    except Exception as e:
        return Response(f'Error: {e}', status=500)

# 根工厂
def rootFactory(request):
    return {}
