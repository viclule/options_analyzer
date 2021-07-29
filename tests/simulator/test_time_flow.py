from datetime import datetime

from options_freedom.simulator.time_flow import TimeFlow


timeflow = TimeFlow(datetime(2006, 1, 6), datetime(2006, 2, 8))
time_generator = timeflow.gen()


def test_time_flow():
    date = next(time_generator)
    assert date == datetime(2006, 1, 6, 15)
    date = next(time_generator)
    assert date == datetime(2006, 1, 9, 15)
