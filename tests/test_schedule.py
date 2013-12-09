"""Raspberry Pi X10 Home Automation schedule object unit tests

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
try:
    import unittest.mock as mock
except ImportError:     # Python < 3.3
    import mock


def _get_one():
    from raspi_x10.schedule import Schedule
    return Schedule


def _make_one():
    return _get_one()()


def test_add_macro():
    sched = _make_one()
    sched.devices = {'foo': 'A1'}
    sched._add_macro('foo', 'on')
    assert 'macro fooOn on A1' in sched.macros


def test_write_macros():
    sched = _make_one()
    sched.devices = {'foo': 'A1'}
    sched._add_macro('foo', 'on')
    sched._add_macro('foo', 'off')
    m = mock.mock_open()
    with mock.patch('raspi_x10.schedule.open', m, create=True):
        sched.write()
    file_obj = m()
    assert mock.call('# Macros:\n') in file_obj.write.mock_calls
    name, args, kwargs = file_obj.writelines.mock_calls[0]
    expected = [
        'macro fooOn on A1\n',
        'macro fooOff off A1\n',
    ]
    for line in expected:
        assert line in args[0]
