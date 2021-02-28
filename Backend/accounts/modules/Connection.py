
from .Threshold import ConnectionThreshold


class Connection:

    def __init__(self, attributes, friendship_duration, mutual_friends=0):
        self.attributes = attributes
        self.friendship_duration = friendship_duration
        self.mutual_friends = mutual_friends

    def __str__(self):
        return "attributes: "+str(self.attributes)+"\n" + "Friendship Duration:"+str(self.friendship_duration) \
               + "\nNumber of Mutual Friends:" + str(self.mutual_friends)

    # def calculate_resemblence_attributes(self, threshold):
    #     count = 0
    #     for field in threshold:
    #         if self.attributes[field] is not None:
    #             if self.attributes[field] == threshold[field]:
    #                 count +=1
    #     return count/len(threshold)

    def set_mutual_friends(self, number_of_friends):
        self.mutual_friends = number_of_friends

    # def set_connection_strength(self, threshold: ConnectionThreshold):
    #     mutual_friends_strength = 1 if self.mutual_friends >= threshold.mutual_friends \
    #         else self.mutual_friends/threshold.mutual_friends
    #     friendship_duration_strength = 1 if self.friendship_duration >= threshold.friendship_duration \
    #         else self.friendship_duration/threshold.friendship_duration
    #     resemblence_attributes = self.calculate_resemblence_attributes(threshold)
    #     self.connection_strength = (mutual_friends_strength + friendship_duration_strength + resemblence_attributes)/3



