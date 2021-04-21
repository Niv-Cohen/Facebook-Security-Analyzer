from . import Threshold, User, Connection
import json
from collections import namedtuple


class Account:
    def __init__(self, name, friends, connection: Connection, user: User):
        self.name = name
        self.friends = friends
        self.connection = connection
        self.user = user

    def __str__(self):
        return "Name: " + str(self.name) + "\n" \
               + str(self.connection) + "\n" + str(self.user) + "\nFriends: " + str(self.get_friends_str())

    def get_friends_str(self):
        for field in self.friends:
            print(field)
            for friend in self.friends[field]:
                print(friend)
                print()

    def set_mutual_friends(self, number_of_friends):
        self.connection.set_mutual_friends(number_of_friends)

    def calc_resemblance_attributes(self, ego_node_attributes):
        resemblance_attributes_counter = 0
        for field in ego_node_attributes:
            if field in self.connection.attributes.keys():
                for info in ego_node_attributes[field]:
                    if self.connection.attributes[field].find(info) != -1:
                        resemblance_attributes_counter += 1
                        break
        return resemblance_attributes_counter

    def set_trust_value(self, threshold: Threshold):
        # Setting UserTrustValue

        total_friends_param = 1 if self.user.total_friends > threshold.user_threshold.total_friends \
            else self.user.total_friends / threshold.user_threshold.total_friends

        age_of_account_param = 1 if self.user.age_of_account > threshold.user_threshold.age_of_account \
            else self.user.age_of_account / threshold.user_threshold.age_of_account

        user_trust_value = (total_friends_param + age_of_account_param) / 2
        # Setting ConnectionTrustValue

        friendship_duration_param = 1 if self.connection.friendship_duration > threshold.connection_threshold.friendship_duration \
            else self.connection.friendship_duration / threshold.connection_threshold.friendship_duration

        mutual_friends_param = 1 if self.connection.mutual_friends > threshold.connection_threshold.mutual_friends \
            else self.connection.mutual_friends / threshold.connection_threshold.mutual_friends

        resemblance_attributes_param = self.calc_resemblance_attributes(threshold.connection_threshold.attributes) \
                                       / len(threshold.connection_threshold.attributes)


        default_param_addition = mutual_friends_param + resemblance_attributes_param

        connection_trust_value = (default_param_addition + friendship_duration_param) / 3 \
            if friendship_duration_param != 0 else default_param_addition / 2
        # Setting Account Overall Trust Value
        if self.name == "Yossi Cohen":
            print("UTV: "+str(user_trust_value))
            print(threshold.connection_threshold.friendship_duration)
            print(friendship_duration_param)
            print("CTV: " + str(connection_trust_value))
            print("resemblance: " + str(resemblance_attributes_param))
        self.account_trust_value = (user_trust_value + connection_trust_value) / 2

    @classmethod
    def from_json(cls, json_string):
        json_dict = json.loads(json_string)
        return cls(**json_dict)


class account_encoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__


def account_decoder(account_dict):
    return namedtuple('X', account_dict.keys())()
