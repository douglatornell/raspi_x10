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
import random
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
        #: List of schedule rules choosen to build today's schedule from
        self._rules_group = []
        #: Mapping of special day mnemonics to date lists
        self.special_days = {}
        #: Heyu x10.sched file macros that each map a device alias and
        #: state string to an X10 command and device code
        self.macros = set()
        #: Heyu x10.sched file timer rule strings
        self.timers = []
        self.today = datetime.datetime.today()

    def load_conf(self, filepath, conf_var, attr):
        """Load data structure from config file into attr.

        :arg filepath: Path and file name of config file.
        :type filepath: str

        :arg conf_var: Variable name of data structure in config file.
        :type conf_var: str

        :arg attr: Attribute name to assign data structure to.
        :type conf_var: str
        """
        try:
            with open(filepath, 'rt') as f:
                source = f.read()
        except IOError:
            log.error('config file not found: {}'.format(filepath))
            raise
        code = compile(source, filepath, 'exec')
        exec(code)
        try:
            setattr(self, attr, locals()[conf_var])
        except KeyError:
            log.error('config variable not found in {}: {}'
                      .format(filepath, conf_var))
            raise

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

    def _is_special_day(self):
        for day in self.special_days:
            for date_str in self.special_days[day]:
                parts = list(map(int, date_str.split('-')))
                if len(parts) == 2:
                    parts.insert(0, self.today.year)
                if datetime.date(*parts) == self.today:
                    return day

    def _choose_rules_group(self, day):
        if day is None or day not in self.rules:
            day = 'Mon Tue Wed Thu Fri Sat Sun'.split()[self.today.weekday()]
        self._rules_group = random.choice(self.rules[day])

    def _handle_absolute_time_event(self, event):
        device, state, time, fuzz = event
        self._add_macro(device, state)
        try:
            parts = list(map(int, time.split(':')))
            start_time = self._calc_fuzzy_time(fuzz, *parts)
            sun_condition = ''
        except AttributeError:
            start_time, sun_condition = self._handle_conditional_time(
                time, fuzz)
        self._add_timer(device, state, start_time, sun_condition)

    def _handle_conditional_time(self, time_condition, fuzz):
        time, offset, sun_condition = time_condition
        if time.lower() in 'dawn dusk'.split():
            offset += random.randint(-fuzz, fuzz)
            start_time = time, offset
        else:
            # Conditional from specific time rather than dawn or dusk
            parts = list(map(int, time.split(':')))
            start_time = self._calc_fuzzy_time(fuzz, *parts, offset=offset)
        return start_time, sun_condition

    def _add_macro(self, device, state):
        macro_name = device + state.capitalize()
        self.macros.add('macro {} {} {}'
            .format(macro_name, state, self.devices[device]))

    def _calc_fuzzy_time(self, fuzz, hour, minute, offset=0):
        fuzzy_time = self.today.replace(hour=hour, minute=minute)
        fuzzy_time += datetime.timedelta(minutes=offset)
        fuzz = datetime.timedelta(minutes=random.randint(-fuzz, fuzz))
        fuzzy_time += fuzz
        return fuzzy_time

    def _add_timer(self, device, state, start_time, sun_condition=''):
        macro_name = device + state.capitalize()
        strt_date = self.today
        end_date = self.today + datetime.timedelta(days=7)
        try:
            strt_time = '{:%H:%M}'.format(start_time)
        except ValueError:
            try:
                strt_time = '{0[1]}{0[2]:+d}'.format(start_time)
            except IndexError:
                strt_time = '{0[0]}{0[1]:+d}'.format(start_time)
        timer = (
            'timer smtwtfs {0:%m/%d}-{1:%m/%d} {2} 23:59 {3} null'
            .format(strt_date, end_date, strt_time, macro_name))
        if sun_condition:
            timer = ' '.join((timer, sun_condition))
        self.timers.append(timer)


if __name__ == '__main__':
    devices_file, rules_file, special_days_file = sys.argv[1:]
    sched = Schedule()
    try:
        sched.load_conf(devices_file, 'x10_devices', 'devices')
        sched.load_conf(rules_file, 'x10_rules', 'rules')
        sched.load_conf(special_days_file, 'special_days', 'special_days')
    except (IOError, KeyError):
        sys.exit(2)
    day = sched._is_special_day()
    sched._choose_rules_group(day)
    import pprint
    pprint.pprint(sched.devices)
    pprint.pprint(sched.rules)
    pprint.pprint(sched.special_days)
    pprint.pprint(sched._rules_group)
