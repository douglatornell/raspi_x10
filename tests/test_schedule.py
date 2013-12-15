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
import datetime
import pytest
try:
    import unittest.mock as mock
except ImportError:     # pragma: no cover; reqd for Python < 3.3
    import mock         # pragma: no cover; reqd for Python < 3.3


def _get_one():
    from raspi_x10.schedule import Schedule
    return Schedule


def _make_one(*kwargs):
    return _get_one()(kwargs)


def test_load_devices():
    sched = _make_one()
    sched._load_conf = mock.Mock(name='_load_conf')
    sched.load_devices('heyu/x10_devices.py')
    sched._load_conf.assert_called_once_with(
        'heyu/x10_devices.py', 'x10_devices')


def test_load_conf_bad_filepath():
    sched = _make_one()
    with pytest.raises(IOError):
        sched._load_conf('foo', 'bar')


def test_load_conf():
    sched = _make_one()
    mock_conf_file = mock.mock_open(read_data='bar = 42')
    with mock.patch('raspi_x10.schedule.open', mock_conf_file, create=True):
        result = sched._load_conf('foo', 'bar')
    assert result == 42


def test_load_conf_bad_conf_var_name():
    sched = _make_one()
    mock_conf = mock.mock_open(read_data='bar = 42')
    with pytest.raises(KeyError):
        with mock.patch('raspi_x10.schedule.open', mock_conf, create=True):
            sched._load_conf('foo', 'baz')


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


def test_write_timers():
    sched = _make_one()
    sched.devices = {'foo': 'A1'}
    start_time = datetime.datetime(2013, 12, 8, 20, 1, 0)
    end_date = datetime.date(2013, 12, 15)
    sched._add_timer('foo', 'on', start_time, end_date)
    sched._add_timer('foo', 'on', start_time, end_date)
    m = mock.mock_open()
    with mock.patch('raspi_x10.schedule.open', m, create=True):
        sched.write()
    file_obj = m()
    assert mock.call('\n# Timers:\n') in file_obj.write.mock_calls
    expected = [
        'timer smtwtfs 12/08-12/15 20:01 23:59 fooOn null\n',
        'timer smtwtfs 12/08-12/15 20:01 23:59 fooOn null\n',
    ]
    name, args, kwargs = file_obj.writelines.mock_calls[1]
    assert args[0] == expected


def test_add_macro():
    sched = _make_one()
    sched.devices = {'foo': 'A1'}
    sched.devices = {'foo': 'A1'}
    sched._add_macro('foo', 'on')
    assert 'macro fooOn on A1' in sched.macros


def test_add_timer_absolute_start_time():
    sched = _make_one()
    sched.devices = {'foo': 'A1'}
    start_time = datetime.datetime(2013, 12, 8, 20, 1, 0)
    end_date = datetime.date(2013, 12, 15)
    sched._add_timer('foo', 'on', start_time, end_date)
    assert 'timer smtwtfs 12/08-12/15 20:01 23:59 fooOn null' in sched.timers


def test_add_timer_sun_condition():
    sched = _make_one()
    sched.devices = {'foo': 'A1'}
    start_time = datetime.datetime(2013, 12, 8, 20, 1, 0)
    end_date = datetime.date(2013, 12, 15)
    sched._add_timer('foo', 'on', start_time, end_date, 'dawngt 05:45')
    expected = 'timer smtwtfs 12/08-12/15 20:01 23:59 fooOn null dawngt 05:45'
    assert expected in sched.timers


def test_add_timer_start_time_after_dawn():
    sched = _make_one()
    sched.devices = {'foo': 'A1'}
    start_time = (datetime.datetime(2013, 12, 8, 20, 1, 0), 'dawn', 42)
    end_date = datetime.date(2013, 12, 15)
    sched._add_timer('foo', 'on', start_time, end_date)
    assert 'timer smtwtfs 12/08-12/15 dawn+42 23:59 fooOn null' in sched.timers


def test_add_timer_start_time_before_dusk():
    sched = _make_one()
    sched.devices = {'foo': 'A1'}
    start_time = (datetime.datetime(2013, 12, 8, 20, 1, 0), 'dusk', -42)
    end_date = datetime.date(2013, 12, 15)
    sched._add_timer('foo', 'on', start_time, end_date)
    assert 'timer smtwtfs 12/08-12/15 dusk-42 23:59 fooOn null' in sched.timers
