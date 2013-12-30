"""Raspberry Pi X10 Home Automation web remote control app

Copyright 2013 Doug Latornell

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import logging
import subprocess
import sys
import os
import wsgiref.simple_server
import pyramid.config
import pyramid.view


logging.basicConfig()
log = logging.getLogger('web_remote')

here = os.path.dirname(os.path.abspath(__file__))

away_mode = False


@pyramid.view.view_config(route_name='home', renderer='home.mako')
def home_view(request):
    context = {}
    return context


@pyramid.view.view_config(route_name='away_mode', renderer='json')
def away_mode_view(request):
    return {'AwayMode': toggle_away_mode()}


@pyramid.view.view_config(route_name='status', renderer='json')
def status_view(request):
    return get_status()


def toggle_away_mode():
    global away_mode
    away_mode = not away_mode
    return away_mode


def get_status():
    cmd = 'heyu onstate AwayMode'.split()
    away_mode = subprocess.check_output(cmd, universal_newlines=True).strip()
    return {'AwayMode': away_mode != '0'}


def main(argv=[__name__]):
    debug = 'debug' in argv
    if debug:
        settings = {
            'debug_all': True,
        }
        log.setLevel(logging.DEBUG)
        log.debug('debugging enabled')
    else:
        settings = {}
    settings['mako.directories'] = os.path.join(here, 'templates')
    config = pyramid.config.Configurator(settings=settings)
    config.include('pyramid_mako')
    config.add_static_view('static', os.path.join(here, 'static'))
    config.add_route('home', '/')
    config.add_route('away_mode', '/away_mode')
    config.add_route('status', '/status')
    config.scan()
    app = config.make_wsgi_app()
    server = wsgiref.simple_server.make_server('0.0.0.0', 6543, app)
    server.serve_forever()


if __name__ == '__main__':
    sys.exit(main(sys.argv))    # pragma: no cover
