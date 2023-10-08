from typing import Generator


def filter_movie(request) -> str:
    order_generator: Generator = request.GET.items()
    order_type: str = 'title'
    for item in order_generator:
        order_type = item[0]
    return order_type
