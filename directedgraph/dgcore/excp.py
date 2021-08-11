class GroundNodeNumberError(Exception):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


class ArcError(Exception):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message
