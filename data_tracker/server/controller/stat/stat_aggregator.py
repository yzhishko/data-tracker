import math
from collections import deque
from typing import List

from pydantic import BaseModel

from data_tracker.config import TRACK_WINDOW_MILLIS
from data_tracker.server.controller.stat.stat_change_listener import StatChangeListener


class RegisteredPrice(BaseModel):
    time: int
    price: float


class StatAggregator:

    def __init__(self, pair: str):
        """
            Crypto pair
        :param pair:
        """
        self._pair = pair
        self._stat_change_listeners: List[StatChangeListener] = []
        # Holds sliding window sum of prices
        self._window_price_sum = 0
        # Holds sliding window number of elements in a queue
        self._window_price_number = 0
        # Holds sliding window sum of squares of prices
        self._window_square_price_sum = 0
        # Queue of prices in sliding window
        self._price_queue = deque()
        # Current standard deviation
        self._std_deviation = 0

    def add_pair_price(self, time: int, price: float):
        """
            Register a pair of time and price for specific crypto, calculates the standard deviation.
            See the README for standard deviation sliding window compute.
        :param time:
        :param price:
        :return:
        """
        time_for_evict = time - TRACK_WINDOW_MILLIS
        while self._price_queue and self._price_queue[0].time < time_for_evict:
            registered_price: RegisteredPrice = self._price_queue.popleft()
            self._window_price_number -= 1
            self._window_price_sum -= registered_price.price
            self._window_square_price_sum -= registered_price.price * registered_price.price
        old_std_deviation = self._std_deviation
        self._window_price_number += 1
        self._window_price_sum += price
        self._window_square_price_sum += price * price
        variance = (self._window_square_price_sum - self._window_price_sum * self._window_price_sum /
                    self._window_price_number) / self._window_price_number
        self._std_deviation = math.sqrt(variance) if variance else 0
        self._price_queue.append(RegisteredPrice(time=time, price=price))
        for listener in self._stat_change_listeners:
            listener.std_deviation_changed(self._pair, old_std_deviation, self._std_deviation)

    def get_prices(self) -> List[RegisteredPrice]:
        """
            Returns a list of prices and times they were registered at
        :return:
        """
        return list(self._price_queue)

    def register_listener(self, listener: StatChangeListener):
        f"""
            Add an instance of {StatChangeListener} 
        :param listener: {StatChangeListener} instance
        :return: 
        """
        self._stat_change_listeners.append(listener)
