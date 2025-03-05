pagination_fields = ('limit', 'offset')


class Query:
    def __init__(self, query_params: dict):
        self.filters: dict = {
            key: value
            for key, value in query_params.items()
            if key not in pagination_fields
        }
        self.limit = (
            int(query_params['limit']) if 'limit' in query_params else None
        )
        self.offset = int(query_params.get('offset', 0))

    def __str__(self):
        return (
            f'(filters={self.filters}, limit={self.limit}, '
            'offset={self.offset})'
        )
