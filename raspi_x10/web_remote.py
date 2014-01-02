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
import os
import pyramid.config
import pyramid.view
import raspi_x10.schedule


logging.basicConfig()
log = logging.getLogger(__name__)

here = os.path.dirname(os.path.abspath(__file__))

heyu_state_toggle_cmd = {
    True: 'off',
    False: 'on',
}
away_mode_state_rules = {
    True: 'away_mode_rules.py',
    False: 'people_home_rules.py',
}


@pyramid.view.view_config(route_name='home', renderer='home.mako')
def home_view(request):
    context = {}
    return context


@pyramid.view.view_config(route_name='away_mode', renderer='json')
def away_mode_view(request):
    return {'AwayMode': toggle_away_mode()}


@pyramid.view.view_config(route_name='status', renderer='json')
def status_view(request):
    return get_state()


def toggle_away_mode():
    state = get_state()
    cmd = 'heyu {} AwayMode'.format(heyu_state_toggle_cmd[state['AwayMode']])
    subprocess.check_call(cmd.split())
    state['AwayMode'] = not state['AwayMode']
    rules = away_mode_state_rules[state['AwayMode']]
    args = [
        'schedule',
        'heyu/x10_devices.py',
        'heyu/{}'.format(rules),
        'heyu/special_days.py',
    ]
    raspi_x10.schedule.main(args)
    cmd = 'heyu upload'
    subprocess.check_call(cmd.split())
    cmd = 'heyu catchup'
    subprocess.check_call(cmd.split())
    return state['AwayMode']


def get_state():
    cmd = 'heyu onstate AwayMode'
    away_mode = subprocess.check_output(
        cmd.split(), universal_newlines=True).strip()
    return {'AwayMode': away_mode != '0'}


def main(global_config, **settings):
    config = pyramid.config.Configurator(settings=settings)
    config.add_static_view('static', os.path.join(here, 'static'))
    config.add_route('home', '/')
    config.add_route('away_mode', '/away_mode')
    config.add_route('status', '/status')
    config.scan()
    app = config.make_wsgi_app()
    return app
