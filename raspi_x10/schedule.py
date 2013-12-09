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
    def __init__(self, sched_file='/home/pi/.heyu/x10.sched'):
        """
        :arg sched_file: File path and name of the Heyu schedule file to write.
        :type sched_file: str
        """
        self.sched_file = sched_file
        #: Heyu x10.sched file macros that each map a device name and
        #: state string to an X10 command and device code
        self.macros = set()
        #: Heyu x10.sched file timer rule strings
        self.timers = []

    def write(self):
        """Write the Heyu schedule file.
        """
        with open(self.sched_file, 'w') as f:
            f.write('# Macros:\n')
            macros = ['{}\n'.format(m) for m in self.macros]
            f.writelines(macros)
            f.write('\n# Timers:\n')
            timers = ['{}\n'.format(t) for t in self.timers]
            f.writelines(timers)

    def _add_macro(self, device, state):
        macro_name = device + state.capitalize()
        self.macros.add('macro {} {} {}'
            .format(macro_name, state, self.devices[device]))

    def _add_timer(self, device, state, start_time, end_date,
                   sun_condition=''):
        macro_name = device + state.capitalize()
        try:
            strt_date = '{:%m/%d}'.format(start_time)
            strt_time = '{:%H:%M}'.format(start_time)
        except ValueError:
            strt_date = '{[0]:%m/%d}'.format(start_time)
            strt_time = '{0[1]}{0[2]:+d}'.format(start_time)
        timer = (
            'timer smtwtfs {0}-{1:%m/%d} {2} 23:59 {3} null'
            .format(strt_date, end_date, strt_time, macro_name))
        if sun_condition:
            timer = ' '.join((timer, sun_condition))
        self.timers.append(timer)
