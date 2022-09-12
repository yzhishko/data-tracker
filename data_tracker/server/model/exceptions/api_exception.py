class APIException(Exception):

    # TODO: add more constructor args (cause, etc.)
    def __init__(self, msg):
        super().__init__(msg)
        self._msg = msg

    @property
    def message(self):
        return self._msg
