from seed import paginate_users

def lazy_paginate(page_size):
    offset = 0
    while True:
        rows = paginate_users(page_size, offset)
        if not rows:
            break
        yield rows
        offset += page_size