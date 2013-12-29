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
import sys
import os
import wsgiref.simple_server
import pyramid.config
import pyramid.view


logging.basicConfig()
log = logging.getLogger(__file__)

here = os.path.dirname(os.path.abspath(__file__))


@pyramid.view.view_config(route_name='home', renderer='home.mako')
def home_view(request):
    context = {}
    return context


def main(argv=[__name__]):
    if argv[1] == 'debug':
        settings = {
            'reload_all': True,
            'debug_all': True,
        }
    else:
        settings = {}
    settings['mako.directories'] = os.path.join(here, 'templates')
    config = pyramid.config.Configurator(settings=settings)
    config.include('pyramid_mako')
    config.add_static_view('static', os.path.join(here, 'static'))
    config.add_route('home', '/')
    config.scan()
    app = config.make_wsgi_app()
    server = wsgiref.simple_server.make_server('0.0.0.0', 6543, app)
    server.serve_forever()


if __name__ == '__main__':
    sys.exit(main(sys.argv))    # pragma: no cover
