def trim(list: list, start: int, end: int):
    '''
    Trim a list of items to a specific range.
    '''
    return list[start:end]

def pagination_string(list: list, start: int, end: int):
    '''
    Get the pagination string for a list of items. This will return the page the user is in, the number of items per page, and the total number of items.
    format: "start-end/total"
    '''
    if end > len(list):
        end = len(list)
    return f'{start + 1}-{end}/{len(list)}'

def complete_pagination(list: list, skip: int, limit: int):
    '''
    Get the pagination string for a list of items. This will return the page the user is in, the number of items per page, and the total number of items.
    format: "start-end/total"
    '''
    return pagination_string(list, skip, skip + limit), trim(list, skip, skip + limit)