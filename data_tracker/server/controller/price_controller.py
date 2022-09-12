import logging

import aiohttp

from data_tracker.config import EXCHANGE_REQUEST_URL, EXCHANGE
from data_tracker.server.controller.stat.stat_collector import StatCollector
from data_tracker.server.model.exceptions.api_exception import APIException
from data_tracker.server.model.messages.v1 import CryptoPriceV1


class PriceController:

    def __init__(self, stat_collector: StatCollector):
        self._stat_collector = stat_collector
        self._logger = logging.getLogger()

    async def get_prices_with_rank(self, pair: str):
        prices = self._stat_collector.get_prices(pair)
        rank = self._stat_collector.get_rank(pair)
        return CryptoPriceV1(prices=prices, rank=rank[0], total_pairs=rank[1])

    async def get_pairs(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(EXCHANGE_REQUEST_URL.format(EXCHANGE)) as response:
                if response.status != 200:
                    res = await response.text()
                    raise APIException(res)
                else:
                    res = await response.json()
                    pairs = []
                    for it in res["result"]:
                        pairs.append(it["pair"])
                    return pairs
