from datetime import datetime

class CacheObject:
    date: dict[str, datetime] = None
    value = None
    update_function = None
    update_interval:float = 60

    def __init__(self, update_function, updateInterval=60):
        self.update_function = update_function
        self.date = {}
        self.value = {}
        self.update_interval = updateInterval

    def get(self, **kwargs):
        if len(kwargs) == 0:
            argsHash = "None"
        else:
            argsHash = hash(tuple(kwargs.items()))
        if argsHash not in self.date or (datetime.now() - self.date[argsHash]).total_seconds() > self.update_interval:
            self.value[argsHash] = self.update_function(**kwargs)
            self.date[argsHash] = datetime.now()
        return self.value[argsHash]

class Caches:
    def __init__(self):
        self.cache = {}

    def add(self, key, update_function, updateInterval=60):
        self.cache[key] = CacheObject(update_function, updateInterval)

    def get(self, key, **kwargs):
        return self.cache[key].get(**kwargs)

cachedData = Caches()