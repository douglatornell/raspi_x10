"""Raspberry Pi X10 Home Automation schedule object

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


class Schedule():
    """Heyu schedule object.
    """
    def __init__(self):
        #: Heyu x10.sched file macros that each map a device name and
        #: state string to an X10 command and device code
        self.macros = set()
        #: Heyu x10.sched file timer rule strings
        self.timers = []

    def _add_macro(self, device, state):
        macro_name = device + state.capitalize()
        self.macros.add('macro {} {} {}'
            .format(macro_name, state, self.devices[device]))
