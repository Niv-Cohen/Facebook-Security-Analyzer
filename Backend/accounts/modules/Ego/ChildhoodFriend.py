from .Colleague import Colleague


class ChildhoodFriend(Colleague):
    permissions = Colleague.permissions + ['Commenting']
