from dependency_injector import containers, providers

from data_tracker.server.controller.price_controller import PriceController
from data_tracker.server.controller.stat.ranker import Ranker
from data_tracker.server.controller.stat.stat_collector import StatCollector
from data_tracker.server.worker.crypto_update_worker import CryptoUpdateWorker


class RankerInstance(containers.DeclarativeContainer):
    get = providers.Singleton(
        Ranker
    )


class StatCollectorInstance(containers.DeclarativeContainer):
    get = providers.Singleton(
        StatCollector, ranker=RankerInstance.get
    )


class PriceControllerInstance(containers.DeclarativeContainer):
    get = providers.Singleton(
        PriceController, stat_collector=StatCollectorInstance.get
    )


class CryptoUpdateWorkerInstance(containers.DeclarativeContainer):
    get = providers.Singleton(
        CryptoUpdateWorker, stat_collector=StatCollectorInstance.get
    )
