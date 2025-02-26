# pagination.py

def paginate_query(page, page_size):
    try:
        page = int(page) if page and int(page) > 0 else 1
        page_size = int(page_size) if page_size and int(page_size) > 0 else 10
    except ValueError:
        page, page_size = 1, 10
    offset = (page - 1) * page_size
    return page_size, offset
