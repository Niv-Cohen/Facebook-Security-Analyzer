from .Friend import Friend


class Colleague(Friend):
    permissions = Friend.permissions + ['Seeing Attributes']
