# from datetime import datetime, timedelta

# from options_freedom.pattern.bull_put_spread import BullPutSpread
# from options_freedom.symbol.base import Symbol
# from options_freedom.option.spy import spy
# from options_freedom.option.base import Type


# today = datetime(2006, 1, 4)
# # days for expiration target
# expiration_target = timedelta(days=45)
# # delta for the legs
# delta_short_put = 0.30
# delta_long_put = 0.15


# short_put = spy.get_option(Type.P, today, today + expiration_target, delta_short_put)
# long_put = spy.get_option(Type.P, today, today + expiration_target, delta_long_put)

# pattern = BullPutSpread(
#     symbol=Symbol(symbol="SPY"),
#     short=[short_put],
#     long=[long_put],
# )


# def test_max_loss():
#     assert pattern.max_loss == 3
