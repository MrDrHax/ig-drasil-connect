from tools.lazySquirrel import LazySquirrel

class QueryParams:
    def __init__(self, q: str | None = None, skip: int = 0, limit: int = 100, sortByDat: str | None = None, sortBy: str = 'asc'):
        self.q = q
        self.skip = skip
        self.limit = limit
        if not sortByDat or not sortBy:
            self.sortBy = None
        else:
            self.sortBy = (sortByDat, sortBy)

    def apply(self, data: list):
        ls = LazySquirrel(data)
        
        if self.q:
            filtering = self.q.split(',')
            
            for f in filtering:
                key, value = f.split('=')
                ls.filter_by(key, value)
        
        if self.sortBy:
            ls.sort_by(self.sortBy[0], self.sortBy[1] == 'desc')
        
        return ls.paginate(self.skip, self.limit)