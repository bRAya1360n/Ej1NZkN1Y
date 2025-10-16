# 代码生成时间: 2025-10-16 23:31:58
# breadcrumbs.py

"""
A Pyramid breadcrumbs component.
"""

from pyramid.response import Response
from pyramid.view import view_config
from pyramid.renderers import render_to_response
from pyramid.threadlocal import get_current_request


# Define the breadcrumb class
class Breadcrumbs:
    def __init__(self):
        # Initialize an empty list to store breadcrumb links
        self.breadcrumbs = []

    def add(self, name, url):
        """Add a breadcrumb with a name and URL."""
        if not name or not url:
            raise ValueError("Name and URL cannot be empty")
        self.breadcrumbs.append((name, url))

    def remove(self, index):
        """Remove a breadcrumb at a specified index."""
        if index < 0 or index >= len(self.breadcrumbs):
            raise IndexError("Index out of range")
        del self.breadcrumbs[index]

    def get_breadcrumbs(self):
        """Get the current list of breadcrumbs."""
        return self.breadcrumbs


# Pyramid view to render breadcrumbs
@view_config(route_name='breadcrumbs', renderer='json')
def breadcrumbs_view(request):
    """
    View function to provide the breadcrumbs data.

    This function is connected to the 'breadcrumbs' route and returns
    the current breadcrumbs as a JSON response.
    """
    # Get the breadcrumbs object from the request registry
    breadcrumbs = request.registry.breadcrumbs
    # Return the breadcrumbs data as JSON
    return breadcrumbs.get_breadcrumbs()


# Pyramid configuration
def main(global_config, **settings):
    """
    Pyramid main function to set up the application.

    This function sets up the application configuration and
    initializes the breadcrumbs component.
    """
    config = Configurator(settings=settings)

    # Initialize the breadcrumbs object and add it to the request registry
    config.registry.breadcrumbs = Breadcrumbs()

    # Add some initial breadcrumbs
    config.registry.breadcrumbs.add("Home", "/")
    config.registry.breadcrumbs.add("Products", "/products")

    # Scan for @view_config decorators, etc.
    config.scan()

    return config.make_wsgi_app()
