from data_tracker.server.controller.stat.ranker import Ranker
from data_tracker.server.controller.stat.stat_aggregator import RegisteredPrice
from data_tracker.server.controller.stat.stat_collector import StatCollector


# TODO: Add more tests by mocking Crypto Watch api calls
def test_stat_collector_ranking():
    stat_collector = StatCollector(Ranker())
    stat_collector.add_pair_price(0, "BTCUSD", 10000)
    assert (1, 1) == stat_collector.get_rank("BTCUSD")
    stat_collector.add_pair_price(1, "BTCUSD", 20000)
    assert (1, 1) == stat_collector.get_rank("BTCUSD")
    stat_collector.add_pair_price(0, "BTCEUR", 12000)
    stat_collector.add_pair_price(1, "BTCEUR", 18000)
    # The BTCUSD rank should be increased, since it has the highest std deviation
    assert (1, 2) == stat_collector.get_rank("BTCEUR")
    assert (2, 2) == stat_collector.get_rank("BTCUSD")
    assert [RegisteredPrice(time=0, price=10000), RegisteredPrice(time=1, price=20000)] == \
           stat_collector.get_prices("BTCUSD")
    assert [RegisteredPrice(time=0, price=12000), RegisteredPrice(time=1, price=18000)] == \
           stat_collector.get_prices("BTCEUR")


def test_expired_price():
    # We don't store prices older than 24 hours back in time
    stat_collector = StatCollector(Ranker())
    stat_collector.add_pair_price(0, "BTCUSD", 10000)
    stat_collector.add_pair_price(1, "BTCUSD", 20000)
    stat_collector.add_pair_price(86400001, "BTCUSD", 7000)
    stat_collector.add_pair_price(86400005, "BTCUSD", 8000)
    assert [RegisteredPrice(time=86400001, price=7000), RegisteredPrice(time=86400005, price=8000)] == \
           stat_collector.get_prices("BTCUSD")
