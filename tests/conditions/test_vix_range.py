from datetime import datetime

from options_freedom.conditions.open.vix_range import VIXRange


def test_check_true():
    vix_range = VIXRange(2, 35)
    assert vix_range.can_open(datetime(2006, 1, 4, 15))


def test_check_false():
    vix_range = VIXRange(35, 70)
    assert not vix_range.can_open(datetime(2006, 1, 4, 15))


def test_check_ma():
    vix_range = VIXRange(0, 15)
    assert not vix_range.can_open(datetime(2006, 7, 3, 15))
