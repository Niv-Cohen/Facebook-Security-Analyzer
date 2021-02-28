from .Threshold import UserThreshold


class User:
    def __init__(self, total_friends, age_of_account):
        self.total_friends = total_friends
        self.age_of_account = age_of_account

    def __str__(self):
        return "Total Friends: " + str(self.total_friends) + "\nAge Of Account:  " + str(self.age_of_account)

    # def set_trust(self, threshold: UserThreshold):
    #     total_friends_strength = 1 if self.total_friends >= threshold.total_friends \
    #         else self.total_friends / threshold.total_friends
    #     age_of_account_strength = 1 if self.age_of_account >= threshold.age_of_account \
    #         else self.age_of_account / threshold.age_of_account
    #     self.user_strength = (total_friends_strength + age_of_account_strength) / 2
