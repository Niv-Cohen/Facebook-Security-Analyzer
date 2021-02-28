from .Colleague import Colleague


class CoStudent(Colleague):
    permissions = Colleague.permissions + ['Commenting']
