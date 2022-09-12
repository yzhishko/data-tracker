from fastapi import APIRouter
from fastapi_versioning import version

from data_tracker.server.dependencies.singletons import PriceControllerInstance, CryptoUpdateWorkerInstance

router = APIRouter()


@router.get('/statistic', description="Return the list prices with their respective timestamps in millis and rank")
@version(1)
async def get_prices_with_rank(pair: str):
    await CryptoUpdateWorkerInstance.get().watch_crypto(pair)
    return await PriceControllerInstance.get().get_prices_with_rank(pair)


@router.get('/pairs', description="Return all pairs for the crypto exchange")
@version(1)
async def get_pairs():
    return await PriceControllerInstance.get().get_pairs()
