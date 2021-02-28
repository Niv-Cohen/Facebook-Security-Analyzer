from .General import General


class Friend(General):

    permissions = General.permissions + \
        ['Seeing Posts', 'Seeing Pictures']
