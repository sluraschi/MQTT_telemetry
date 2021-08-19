
class Payload:
    def to_dict(self):
        raise NotImplementedError

    def to_tuple(self):
        raise NotImplementedError

    def get_insert_query(self):
        raise NotImplementedError
