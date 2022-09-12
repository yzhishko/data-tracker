from typing import List

from pydantic import BaseModel

from data_tracker.server.controller.stat.stat_aggregator import RegisteredPrice


class CryptoPriceV1(BaseModel):
    prices: List[RegisteredPrice]
    rank: int
    total_pairs: int
