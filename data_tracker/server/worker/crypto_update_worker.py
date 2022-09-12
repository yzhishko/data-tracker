import asyncio
import logging
import time

import aiohttp
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from data_tracker.config import PRICE_REQUEST_URL, EXCHANGE, REQUEST_PRICE_INTERVAL_SECONDS
from data_tracker.server.controller.stat.stat_collector import StatCollector


class CryptoUpdateWorker:
    f"""
        A singleton is responsible to schedule a job to grab the latest price and update the {StatCollector}
    """

    def __init__(self, stat_collector: StatCollector):
        self._scheduler = AsyncIOScheduler()
        self._stat_collector = stat_collector
        self._logger = logging.getLogger()
        self._job_map = {}

    def start(self):
        """
            Start the scheduler
        :return:
        """
        self._scheduler.start()

    async def request_prices(self, pair: str):
        f"""
            Request a price for a specific pair and add it to {StatCollector} instance
        :param pair: crypto pair to check
        :return:
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(PRICE_REQUEST_URL.format(EXCHANGE, pair)) as response:
                # These logging events will be collected for failures debugging
                if response.status != 200:
                    self._logger.warning(await response.text())
                else:
                    res = await response.json()
                    self._stat_collector.add_pair_price(round(time.time() * 1000), pair, res["result"]["price"])

    def shutdown(self):
        """
            Shut the scheduler down
        :return:
        """
        self._scheduler.shutdown()

    async def watch_crypto(self, pair):
        """
            Add job if not exists to grab latest price for crypto in a specified interval
        :param pair: crypto pair
        :return:
        """
        if pair not in self._job_map:
            await asyncio.wait([self.request_prices(pair)])
        # It's possible that 2 calls with the same pair still can get here. We are making sure that only is scheduled
        # for execution
        if pair not in self._job_map:
            self._job_map[pair] = self._scheduler.add_job(self.request_prices, 'interval',
                                                          seconds=REQUEST_PRICE_INTERVAL_SECONDS, kwargs={"pair": pair})
