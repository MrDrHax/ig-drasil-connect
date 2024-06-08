import typing

def pagination_string(list: list, start: int, end: int):
    '''
    Get the pagination string for a list of items. This will return the page the user is in, the number of items per page, and the total number of items.
    format: "start-end/total"
    '''
    if len(list) == 0:
        return "1-1/1"
    if end > len(list):
        end = len(list)
    return f'{start + 1}-{end}/{len(list)}'

class LazySquirrel:
    def __init__(self, data: list):
        self.data = data
        self.operations = []
    
    def sort_by(self, key, reverse=False):
        self.operations.append(lambda x: sorted(x, key=lambda item: item[key], reverse=reverse))
        return self
    
    def filter_by(self, key, value):
        '''Match an object in the value. (using value in str(x[key]))'''
        if isinstance(value, int):
            self.operations.append(lambda x: [item for item in x if value == item[key]])
        elif isinstance(value, str):
            self.operations.append(
                lambda x: [item for item in x if str(value).lower() in str(item[key]).lower()]
                )
            
        elif isinstance(value, list):
            self.operations.append(lambda x: [item for item in x if item[key] in value])
        else:
            self.operations.append(lambda x: [item for item in x if value == item[key]])
            
        return self

    def filter_by_range(self, key, start, end):
        self.operations.append(lambda x: [item for item in x if start <= item[key] <= end])
        return self
    
    def add_operation(self, operation: typing.Callable):
        self.operations.append(operation)
        return self

    def paginate(self, skip, limit):
        result = self.get()
        paginated_result = result[skip:skip + limit]
        return pagination_string(result, skip, skip + limit), paginated_result
    
    def get(self):
        result = self.data
        for operation in self.operations:
            result = operation(result)
        return result

    
if __name__ == "__main__":
    testdata = [
        {"name": "John", "age": 23},
        {"name": "Jane", "age": 22},
        {"name": "Smith", "age": 27},
        {"name": "Doe", "age": 25},
    ]

    ls = LazySquirrel(testdata)

    ans = ls.sort_by("age", reverse=True).filter_by('name', 'J').paginate(0, 5)
    print(ans)