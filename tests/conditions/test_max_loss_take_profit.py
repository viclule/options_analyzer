from options_freedom.conditions.close.max_loss_take_profit import MaxLossTakeProfit


def test_check_max_loss():
    close = MaxLossTakeProfit(50, 100)
    assert close.can_close(-2, 3)


def test_check_take_profit():
    close = MaxLossTakeProfit(50, 100)
    assert close.can_close(7, 3)


def test_check_continue():
    close = MaxLossTakeProfit(50, 100)
    assert not close.can_close(-1, 3)
    assert not close.can_close(2.5, 3)
