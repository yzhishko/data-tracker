from typing import Tuple

from data_tracker.server.controller.stat.stat_change_listener import StatChangeListener


class Ranker(StatChangeListener):

    def __init__(self):
        self._ranking_list = []
        self._ranking_map = {}

    def get_rank(self, pair: str) -> Tuple[int, int]:
        """
            Return rank for request crypto pair
        :param pair: crypto pair
        :return: tuple of the rank and total number of pairs we track
        """
        # Find current position in ranking list in O(1)
        return (self._ranking_map[pair] + 1, len(self._ranking_list)) if pair in self._ranking_map else (0, 0)

    def _update_existing_rank(self, pair: str, old_std_deviation: float, new_std_deviation: float):
        current_pos = self._ranking_map[pair]
        if new_std_deviation > old_std_deviation:
            # Shift existing ranks to left and insert new rank for a pair in O(len(_ranking_list))
            n = len(self._ranking_list)
            while (current_pos < n and current_pos + 1 < n
                   and new_std_deviation > self._ranking_list[current_pos + 1][0]):
                self._ranking_list[current_pos] = self._ranking_list[current_pos + 1]
                current_pair = self._ranking_list[current_pos][1]
                self._ranking_map[current_pair] -= 1
                current_pos += 1
        else:
            # Shift existing ranks to right and insert new rank for a pair in O(len(_ranking_list))
            while (current_pos >= 0 and current_pos - 1 >= 0
                   and new_std_deviation < self._ranking_list[current_pos - 1][0]):
                self._ranking_list[current_pos] = self._ranking_list[current_pos - 1]
                current_pair = self._ranking_list[current_pos][1]
                self._ranking_map[current_pair] += 1
                current_pos -= 1
        self._ranking_map[pair] = current_pos
        self._ranking_list[current_pos] = (new_std_deviation, pair)

    def _insert_new_rank(self, pair: str, new_std_deviation: float):
        # Find and insert new rank for a pair in O(len(_ranking_list))
        current_pos = len(self._ranking_list) - 1
        while current_pos >= 0 and new_std_deviation < self._ranking_list[current_pos][0]:
            current_pair = self._ranking_list[current_pos][1]
            self._ranking_map[current_pair] += 1
            current_pos -= 1
        self._ranking_map[pair] = current_pos + 1
        self._ranking_list.insert(current_pos+1, (new_std_deviation, pair))

    def std_deviation_changed(self, pair: str, old_std_deviation: float, new_std_deviation: float):
        """
            Update and recompute rank for watched cryptos
        :param pair: crypto pait which deviation has changed
        :param old_std_deviation: old standard deviation
        :param new_std_deviation: new standard deviation
        :return:
        """
        if pair in self._ranking_map:
            self._update_existing_rank(pair, old_std_deviation, new_std_deviation)
        else:
            self._insert_new_rank(pair, new_std_deviation)
