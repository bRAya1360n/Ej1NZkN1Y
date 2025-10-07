# 代码生成时间: 2025-10-07 18:30:37
import logging
from pyramid.config import Configurator
from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPInternalServerError
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the database URI
DATABASE_URI = 'sqlite:///time_series.db'  # Example URI for SQLite

# Create a database engine and session
engine = sa.create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)

# Define the TimeSeries model
class TimeSeriesBase(object):
    __tablename__ = 'time_series'
    id = sa.Column(sa.Integer, primary_key=True)
    timestamp = sa.Column(sa.DateTime, nullable=False)
    value = sa.Column(sa.Float, nullable=False)

# Create the tables
Base = sa.ext.declarative.declarative_base()
Base.metadata.create_all(engine)

# Pyramid view for adding a time series data point
@view_config(route_name='add_data_point', renderer='json')
def add_data_point(request):
    session = Session()
    try:
        # Get parameters from the request
        timestamp = request.matchdict.get('timestamp')
        value = request.matchdict.get('value')

        # Validate the parameters
        if not timestamp or not value:
            raise ValueError('Timestamp and value are required')

        # Create a new time series data point
        data_point = TimeSeriesBase(timestamp=timestamp, value=value)
        session.add(data_point)
        session.commit()
        return {'status': 'success', 'message': 'Data point added'}
    except ValueError as e:
        session.rollback()
        return {'status': 'error', 'message': str(e)}
    except SQLAlchemyError as e:
        session.rollback()
        logger.error('Database error: %s', e)
        raise HTTPInternalServerError('Internal Server Error')
    finally:
        session.close()

# Pyramid view for retrieving time series data
@view_config(route_name='get_data', renderer='json')
def get_data(request):
    session = Session()
    try:
        # Retrieve all time series data points
        data_points = session.query(TimeSeriesBase).all()
        return [{'timestamp': dp.timestamp, 'value': dp.value} for dp in data_points]
    except SQLAlchemyError as e:
        logger.error('Database error: %s', e)
        raise HTTPInternalServerError('Internal Server Error')
    finally:
        session.close()

# Main function to set up the Pyramid application
def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application. """
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.add_route('add_data_point', '/add/:timestamp/:value')
    config.add_route('get_data', '/get')
    config.scan()
    return config.make_wsgi_app()

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    app = main({})
    server = make_server('0.0.0.0', 6543, app)
    logging.info('Serving on http://localhost:6543/')
    server.serve_forever()