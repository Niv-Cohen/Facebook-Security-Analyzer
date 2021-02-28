from .ChildhoodFriend import ChildhoodFriend


class Family(ChildhoodFriend):
    permissions = ChildhoodFriend.permissions + ['Sharing', 'Tagging']
