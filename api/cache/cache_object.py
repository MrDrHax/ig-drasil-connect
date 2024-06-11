import asyncio
from fastapi import FastAPI, BackgroundTasks
from datetime import datetime
from contextlib import asynccontextmanager
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

import logging
logger = logging.getLogger(__name__)

class CacheObject:
    date: dict[str, datetime] = None
    value = None
    update_function = None
    update_interval: float = 60

    def __init__(self, update_function, updateInterval=60):
        self.update_function = update_function
        self.date = {}
        self.value = {}
        self.update_interval = updateInterval

    async def get(self, _force = False, **kwargs):
        # Hash the arguments to store in dict
        if len(kwargs) == 0:
            argsHash = "None"
        else:
            argsHash = hash(tuple(kwargs.items()))

        if _force:
            # Update cache forcefully
            self.value[argsHash] = await self.update_function(**kwargs)
            self.date[argsHash] = datetime.now()
            return self.value[argsHash]

        # Test cache validity
        if argsHash not in self.date or (datetime.now() - self.date[argsHash]).total_seconds() > self.update_interval:
            # Update cache
            self.value[argsHash] = await self.update_function(**kwargs)
            self.date[argsHash] = datetime.now()

        # Return cache
        return self.value[argsHash]
    
    async def invalidateData(self):
        '''Invalidate the cache that is to outdated. The next call to get will update the cache.'''
        outdated_keys = [key for key in self.date if (datetime.now() - self.date[key]).total_seconds() > self.update_interval]
        for key in outdated_keys:
            del self.date[key] 
            del self.value[key]
            await asyncio.sleep(0)

class AutoUpdateCacheObject:
    def __init__(self, updateInterval, functionName) -> None:
        self.updateInterval = updateInterval
        self.functionName = functionName
        self.lastUpdate = datetime.now()

class Caches:
    cache: dict[str, CacheObject] = None
    autoUpdated: list[AutoUpdateCacheObject] = None

    def __init__(self):
        self.cache = {}
        self.autoUpdated = []

    def add(self, key, update_function, updateInterval=60, autoUpdate=False):
        '''Add a function to be cached. The function must be async and return a value. The value will be cached for the updateInterval in seconds.'''
        if autoUpdate:
            self.cache[key] = CacheObject(update_function, updateInterval + 20) # do not invalidate the cache before the auto update
            self.autoUpdated.append(AutoUpdateCacheObject(updateInterval, key))
            return

        self.cache[key] = CacheObject(update_function, updateInterval)

    async def get(self, key, **kwargs):
        '''Get the cached value. If the value is not cached, it will be updated.'''
        return await self.cache[key].get(**kwargs)
    
    async def invalidateData(self):
        '''Invalidate the cache that is to outdated. The next call to get will update the cache.'''
        for key in self.cache:
            await self.cache[key].invalidateData()

    async def triggerAutoUpdates(self):
        '''Trigger all auto update functions to update the cache.'''
        for autoUpdate in self.autoUpdated:
            if (datetime.now() - autoUpdate.lastUpdate).total_seconds() > autoUpdate.updateInterval:
                logger.info(f"Triggering auto update for {autoUpdate.functionName}")
                _ = await self.cache[autoUpdate.functionName].get()
                autoUpdate.lastUpdate = datetime.now()

    async def forceAutoUpdates(self):
        '''Forcefully trigger all auto update functions to update the cache.'''
        logger.info("Restarting auto cached data")
        for autoUpdate in self.autoUpdated:
            logger.info(f"Triggering auto update for {autoUpdate.functionName}")
            _ = await self.cache[autoUpdate.functionName].get()
            autoUpdate.lastUpdate = datetime.now()

# global cache object
cachedData = Caches()

async def invalidate_cache():
    logger.info("Cleaning cache")
    await cachedData.invalidateData()
    logger.info("Cache cleaned")

async def trigger_auto_updates():
    logger.info("Triggering auto updates")
    await cachedData.triggerAutoUpdates()
    logger.info("Auto updates triggered")

async def startup(app: FastAPI, scheduler: AsyncIOScheduler):
    await cachedData.forceAutoUpdates()
    # Start async job
    scheduler.add_job(invalidate_cache, trigger=IntervalTrigger(seconds=60*5)) # clean cache every 5 minutes
    scheduler.add_job(trigger_auto_updates, trigger=IntervalTrigger(seconds=15)) # trigger auto updates every 15 seconds

async def shutdown(app: FastAPI, scheduler: AsyncIOScheduler):
    global cachedData
    # Clean up
    del cachedData