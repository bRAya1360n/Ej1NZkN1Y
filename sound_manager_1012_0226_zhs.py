# 代码生成时间: 2025-10-12 02:26:33
from pyramid.config import Configurator
from pyramid.view import view_config
from pyramid.response import Response
import json

# SoundManager class to handle sound operations
class SoundManager:
    def __init__(self):
        self.sounds = {}

    def add_sound(self, name, path):
        """Add a sound to the manager with its name and path."""
        if name in self.sounds:
            raise ValueError(f"Sound '{name}' already exists.")
        self.sounds[name] = path

    def remove_sound(self, name):
        """Remove a sound from the manager by its name."""
        if name not in self.sounds:
            raise ValueError(f"Sound '{name}' does not exist.")
        del self.sounds[name]

    def get_sound_path(self, name):
        """Get the path of a sound by its name."""
        if name not in self.sounds:
            raise ValueError(f"Sound '{name}' does not exist.")
        return self.sounds[name]

# Pyramid view to handle HTTP requests for sound operations
class SoundManagerView:
    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.sound_manager = SoundManager()

    def add_sound(self):
        data = self.request.json_body
        name = data.get('name')
        path = data.get('path')
        if name is None or path is None:
            return Response(json.dumps({'error': 'Missing name or path'}), content_type='application/json', status=400)
        try:
            self.sound_manager.add_sound(name, path)
            return Response(json.dumps({'message': 'Sound added successfully'}), content_type='application/json', status=200)
        except ValueError as e:
            return Response(json.dumps({'error': str(e)}), content_type='application/json', status=400)

    def remove_sound(self):
        data = self.request.json_body
        name = data.get('name')
        if name is None:
            return Response(json.dumps({'error': 'Missing name'}), content_type='application/json', status=400)
        try:
            self.sound_manager.remove_sound(name)
            return Response(json.dumps({'message': 'Sound removed successfully'}), content_type='application/json', status=200)
        except ValueError as e:
            return Response(json.dumps({'error': str(e)}), content_type='application/json', status=400)

    def get_sound_path(self):
        data = self.request.json_body
        name = data.get('name')
        if name is None:
            return Response(json.dumps({'error': 'Missing name'}), content_type='application/json', status=400)
        try:
            path = self.sound_manager.get_sound_path(name)
            return Response(json.dumps({'path': path}), content_type='application/json', status=200)
        except ValueError as e:
            return Response(json.dumps({'error': str(e)}), content_type='application/json', status=400)

# Pyramid view configuration
def main(global_config, **settings):
    """Create a WSGI app for the Sound Manager."""
    config = Configurator(settings=settings)
    config.add_route('add_sound', '/add_sound')
    config.add_view(SoundManagerView.add_sound, route_name='add_sound', renderer='json')
    config.add_route('remove_sound', '/remove_sound')
    config.add_view(SoundManagerView.remove_sound, route_name='remove_sound', renderer='json')
    config.add_route('get_sound_path', '/get_sound_path')
    config.add_view(SoundManagerView.get_sound_path, route_name='get_sound_path', renderer='json')
    return config.make_wsgi_app()