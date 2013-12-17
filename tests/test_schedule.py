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


def _make_one():
    return _get_one()()


def test_load_conf_bad_filepath():
    sched = _make_one()
    with pytest.raises(IOError):
        sched.load_conf('foo', 'bar', 'baz')


def test_load_conf():
    sched = _make_one()
    mock_conf_file = mock.mock_open(read_data='bar = 42')
    with mock.patch('raspi_x10.schedule.open', mock_conf_file, create=True):
        sched.load_conf('foo', 'bar', 'baz')
    assert sched.baz == 42


def test_load_conf_bad_conf_var_name():
    sched = _make_one()
    mock_conf = mock.mock_open(read_data='bar = 42')
    with pytest.raises(KeyError):
        with mock.patch('raspi_x10.schedule.open', mock_conf, create=True):
            sched.load_conf('foo', 'far', 'baz')


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
    sched.today = datetime.datetime(2013, 12, 8)
    sched.devices = {'foo': 'A1'}
    start_time = datetime.datetime(2013, 12, 8, 20, 1, 0)
    sched._add_timer('foo', 'on', start_time)
    sched._add_timer('foo', 'on', start_time)
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


def test_is_special_day_no_special_days():
    sched = _make_one()
    day = sched._is_special_day()
    assert day is None


def test_is_special_day_year_day_not_today():
    sched = _make_one()
    sched.today = datetime.date(2013, 12, 15)
    sched.special_days = {'EasterSunday': ['2014-04-20']}
    day = sched._is_special_day()
    assert day is None


def test_is_special_day_annual_day_not_today():
    sched = _make_one()
    sched.today = datetime.date(2013, 12, 15)
    sched.special_days = {'NewYears': ['01-01']}
    day = sched._is_special_day()
    assert day is None


def test_is_special_day_today():
    sched = _make_one()
    sched.today = datetime.date(2014, 1, 1)
    sched.special_days = {'NewYears': ['01-01']}
    day = sched._is_special_day()
    assert day == 'NewYears'


def test_choose_rules_group_day_None():
    sched = _make_one()
    sched.today = mock.Mock(weekday=mock.Mock(return_value=6))
    sched.rules['Sun'] = [['foo']]
    sched._choose_rules_group(None)
    assert sched._rules_group == ['foo']


def test_choose_rules_group_special_day_not_in_rules():
    sched = _make_one()
    sched.today = mock.Mock(weekday=mock.Mock(return_value=6))
    sched.rules['Sun'] = [['foo']]
    sched._choose_rules_group('NewYears')
    assert sched._rules_group == ['foo']


def test_choose_rules_group_special_day_in_rules():
    sched = _make_one()
    sched.today = mock.Mock(weekday=mock.Mock(return_value=6))
    sched.rules['NewYears'] = [['foo']]
    sched._choose_rules_group('NewYears')
    assert sched._rules_group == ['foo']


def test_handle_absolute_time_event_adds_macro():
    sched = _make_one()
    sched.today = datetime.datetime(2013, 12, 15)
    sched.devices = {'MstrBedroomLight': 'A1'}
    event = ('MstrBedroomLight', 'off', '07:45', 10)
    sched._handle_absolute_time_event(event)
    assert 'macro MstrBedroomLightOff off A1' in sched.macros


def test_handle_absolute_time_event_adds_timer():
    sched = _make_one()
    sched.today = datetime.datetime(2013, 12, 15)
    sched.devices = {'MstrBedroomLight': 'A1'}
    event = ('MstrBedroomLight', 'off', '07:45', 0)
    sched._handle_absolute_time_event(event)
    expected = 'timer smtwtfs 12/15-12/22 07:45 23:59 MstrBedroomLightOff null'
    assert expected in sched.timers


def test_handle_absolute_time_event_returns_start_time():
    sched = _make_one()
    sched.today = datetime.datetime(2013, 12, 17)
    sched.devices = {'MstrBedroomLight': 'A1'}
    event = ('MstrBedroomLight', 'off', '07:45', 0)
    start_time = sched._handle_absolute_time_event(event)
    assert start_time == datetime.datetime(2013, 12, 17, 7, 45)


def test_handle_absolute_time_event_conditional_time():
    sched = _make_one()
    sched.today = datetime.datetime(2013, 12, 15)
    sched.devices = {'UpperHallLight': 'A1'}
    sched._handle_conditional_time = mock.Mock(
        return_value=(('dawn', 60), 'dawngt 05:45'))
    event = ('UpperHallLight', 'off', ('dawn', 60, 'dawngt 05:45'), 10)
    sched._handle_absolute_time_event(event)
    sched._handle_conditional_time.assert_called_once_with(
        ('dawn', 60, 'dawngt 05:45'), 10)


def test_handle_conditional_time_dawn():
    sched = _make_one()
    start_time, sun_condition = sched._handle_conditional_time(
        ('dawn', 60, 'dawngt 05:45'), 0)
    assert (start_time, sun_condition) == (('dawn', 60), 'dawngt 05:45')


def test_handle_conditional_time_specific_time():
    sched = _make_one()
    sched.today = datetime.datetime(2013, 12, 16)
    start_time, sun_condition = sched._handle_conditional_time(
        ('06:30', 0, 'dawngt 05:45'), 0)
    expected = (datetime.datetime(2013, 12, 16, 6, 30), 'dawngt 05:45')
    assert (start_time, sun_condition) == expected


def test_add_macro():
    sched = _make_one()
    sched.devices = {'foo': 'A1'}
    sched.devices = {'foo': 'A1'}
    sched._add_macro('foo', 'on')
    assert 'macro fooOn on A1' in sched.macros


def test_calc_fuzzy_time_no_fuzz():
    sched = _make_one()
    sched.today = datetime.datetime(2013, 12, 15)
    fuzzy_time = sched._calc_fuzzy_time(0, 20, 38)
    assert fuzzy_time == datetime.datetime(2013, 12, 15, 20, 38)


def test_calc_fuzzy_time():
    sched = _make_one()
    sched.today = datetime.datetime(2013, 12, 15)
    fuzzy_time = sched._calc_fuzzy_time(5, 20, 0)
    expected = (
        fuzzy_time >= datetime.datetime(2013, 12, 15, 19, 55)
        and
        fuzzy_time <= datetime.datetime(2013, 12, 15, 20, 5)
    )
    assert expected


def test_calc_fuzzy_time_with_offset():
    sched = _make_one()
    sched.today = datetime.datetime(2013, 12, 16)
    fuzzy_time = sched._calc_fuzzy_time(0, 8, 52, offset=15)
    assert fuzzy_time == datetime.datetime(2013, 12, 16, 9, 7)


def test_add_timer_absolute_start_time():
    sched = _make_one()
    sched.today = datetime.datetime(2013, 12, 8)
    sched.devices = {'foo': 'A1'}
    start_time = datetime.datetime(2013, 12, 8, 20, 1, 0)
    sched._add_timer('foo', 'on', start_time)
    assert 'timer smtwtfs 12/08-12/15 20:01 23:59 fooOn null' in sched.timers


def test_add_timer_sun_condition():
    sched = _make_one()
    sched.today = datetime.datetime(2013, 12, 8)
    sched.devices = {'foo': 'A1'}
    start_time = datetime.datetime(2013, 12, 8, 20, 1, 0)
    sched._add_timer('foo', 'on', start_time, 'dawngt 05:45')
    expected = 'timer smtwtfs 12/08-12/15 20:01 23:59 fooOn null dawngt 05:45'
    assert expected in sched.timers


def test_add_timer_start_time_after_dawn():
    sched = _make_one()
    sched.today = datetime.datetime(2013, 12, 8)
    sched.devices = {'foo': 'A1'}
    start_time = (datetime.datetime(2013, 12, 8, 20, 1, 0), 'dawn', 42)
    sched._add_timer('foo', 'on', start_time)
    assert 'timer smtwtfs 12/08-12/15 dawn+42 23:59 fooOn null' in sched.timers


def test_add_timer_start_time_before_dusk():
    sched = _make_one()
    sched.today = datetime.datetime(2013, 12, 8)
    sched.devices = {'foo': 'A1'}
    start_time = (datetime.datetime(2013, 12, 8, 20, 1, 0), 'dusk', -42)
    sched._add_timer('foo', 'on', start_time)
    assert 'timer smtwtfs 12/08-12/15 dusk-42 23:59 fooOn null' in sched.timers
