
class ConnectionThreshold:
    def __init__(self, mutual_friends, friendship_duration, attributes):
        self.mutual_friends = mutual_friends
        self.friendship_duration = friendship_duration
        self.attributes = attributes


class UserThreshold:
    def __init__(self, total_friends, age_of_account):
        self.total_friends = total_friends
        self.age_of_account = age_of_account


class Threshold:
    def __init__(self, connection_threshold: ConnectionThreshold, user_threshold: UserThreshold):
        self.connection_threshold = connection_threshold
        self.user_threshold = user_threshold



