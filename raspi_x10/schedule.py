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
import datetime
import logging
import sys


log = logging.getLogger('x10_schedule')
log.setLevel(logging.DEBUG)
stderr = logging.StreamHandler(sys.stderr)
stderr.setLevel(logging.ERROR)
formatter = logging.Formatter('%(message)s')
stderr.setFormatter(formatter)
log.addHandler(stderr)


class Schedule():
    """Heyu schedule object.
    """
    def __init__(
        self,
        sched_file='/home/pi/.heyu/x10.sched',
    ):
        """

        :arg sched_file: File path and name of the Heyu schedule file to write.
        :type sched_file: str
        """
        self.sched_file = sched_file
        #: Mapping of device aliases to X10 device codes
        self.devices = {}
        #: Schedule rules data structure
        self.rules = {}
        #: Mapping of special day mnemonics to date lists
        self.special_days = {}
        #: Heyu x10.sched file macros that each map a device alias and
        #: state string to an X10 command and device code
        self.macros = set()
        #: Heyu x10.sched file timer rule strings
        self.timers = []

    def load_devices(self, devices_file, conf_var='x10_devices'):
        """Load X10 devices data structure from devices config file.

        :arg devices_file: Path and file name of X10 devices config file.
        :type devices_file: str

        :arg conf_var: Variable name of X10 devices data structure in
                       config file; defaults to :py:obj:`x10_devices`.
        :type conf_var: str
        """
        self.devices = self._load_conf(devices_file, conf_var)

    def load_rules(self, rules_file, conf_var='x10_rules'):
        """Load heyu schedule rules data structure from config file.

        :arg rules_file: Path and file name of rules config file.
        :type rules_file: str

        :arg conf_var: Variable name of schedule rules data structure in
                       config file; defaults to :py:obj:`x10_rules`.
        :type conf_var: str
        """
        self.rules = self._load_conf(rules_file, conf_var)

    def load_special_days(self, special_days_file, conf_var='special_days'):
        """Load special dates data structure from config file.

        :arg special_dates_file: Path and file name of special dates
                                 config file.
        :type special_dates_file: str

        :arg conf_var: Variable name of special dates data structure in
                       config file; defaults to :py:obj:`special_dates`.
        :type conf_var: str
        """
        self.special_days = self._load_conf(special_days_file, conf_var)

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

    def _load_conf(self, filepath, conf_var):
        try:
            with open(filepath, 'rt') as f:
                source = f.read()
        except IOError:
            log.error('config file not found: {}'.format(filepath))
            raise
        code = compile(source, filepath, 'exec')
        exec(code)
        try:
            return locals()[conf_var]
        except KeyError:
            log.error('config variable not found in {}: {}'
                      .format(filepath, conf_var))
            raise

    def _is_special_day(self):
        today = datetime.date.today()
        for day in self.special_days:
            for date_str in self.special_days[day]:
                parts = list(map(int, date_str.split('-')))
                if len(parts) == 2:
                    parts.insert(0, today.year)
                if datetime.date(*parts) == today:
                    return day

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


if __name__ == '__main__':
    devices_file, rules_file, special_dates_file = sys.argv[1:]
    sched = Schedule()
    try:
        sched.load_devices(devices_file)
        sched.load_rules(rules_file)
        sched.load_special_dates(special_dates_file)
    except (IOError, KeyError):
        sys.exit(2)
    import pprint
    pprint.pprint(sched.devices)
    pprint.pprint(sched.rules)
    pprint.pprint(sched.special_days)
