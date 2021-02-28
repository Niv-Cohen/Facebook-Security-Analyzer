from .Colleague import Colleague


class Neighbors(Colleague):

    permissions = Colleague.permissions + ['Commenting']
