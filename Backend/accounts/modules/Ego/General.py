
class General:
    permissions = []

    def is_permissioned(cls, action):
        return action in cls.permissions

    def __str__(self):
        return 'My permissions are: ' + str(self.permissions)


