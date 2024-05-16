from datetime import datetime

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

    async def get(self, **kwargs):
        # Hash the arguments to store in dict
        if len(kwargs) == 0:
            argsHash = "None"
        else:
            argsHash = hash(tuple(kwargs.items()))

        # Test cache validity
        if argsHash not in self.date or (datetime.now() - self.date[argsHash]).total_seconds() > self.update_interval:
            # Update cache
            self.value[argsHash] = await self.update_function(**kwargs)
            self.date[argsHash] = datetime.now()

        # Return cache
        return self.value[argsHash]

class Caches:
    def __init__(self):
        self.cache = {}

    def add(self, key, update_function, updateInterval=60):
        '''Add a function to be cached. The function must be async and return a value. The value will be cached for the updateInterval in seconds.'''
        self.cache[key] = CacheObject(update_function, updateInterval)

    async def get(self, key, **kwargs):
        '''Get the cached value. If the value is not cached, it will be updated.'''
        return await self.cache[key].get(**kwargs)

# global cache object
cachedData = Caches()