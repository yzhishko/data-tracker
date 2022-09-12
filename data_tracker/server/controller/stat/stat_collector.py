from typing import List, Tuple

from data_tracker.server.controller.stat.ranker import Ranker
from data_tracker.server.controller.stat.stat_aggregator import StatAggregator, RegisteredPrice


class StatCollector:

    def __init__(self, ranker: Ranker):
        self._stat_aggregator = {}
        self._ranker = ranker

    def add_pair_price(self, time: int, pair: str, price: float):
        if pair not in self._stat_aggregator:
            aggregator = StatAggregator(pair)
            aggregator.register_listener(self._ranker)
            self._stat_aggregator[pair] = aggregator
        self._stat_aggregator[pair].add_pair_price(time, price)

    def get_prices(self, pair: str) -> List[RegisteredPrice]:
        return self._stat_aggregator[pair].get_prices() if pair in self._stat_aggregator else []

    def get_rank(self, pair: str) -> Tuple[int, int]:
        return self._ranker.get_rank(pair)

    def is_tracked(self, pair: str):
        return pair in self._stat_aggregator
