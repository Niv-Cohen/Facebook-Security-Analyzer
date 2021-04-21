import json
from ..modules.Connection import Connection
from ..modules.Account import Account
from ..modules.User import User
from ..Analyze.analyze import filter_network


def parse_rec(account):
    dict = {}
    for field in account["friends"]:
        dict[field] = []
        for i in range(len(account["friends"][field])):
            name = account["friends"][field][i]["name"]
            connection = account["friends"][field][i]["connection"]
            connection = Connection(connection["attributes"], connection["friendship_duration"], connection["mutual_friends"])
            user = account["friends"][field][i]["user"]
            user = User(user["total_friends"], user["age_of_account"])
            friends = parse_rec(account["friends"][field][i])
            dict[field].append(Account(name, friends, connection, user))
    return dict


def parse_user(json_user):
    json_user = json.loads(json_user)
    friends = parse_rec(json_user)
    user = User(**json_user["user"])
    connection = Connection(**json_user["connection"])
    return Account(json_user["name"], friends, connection, user)


if __name__ == '__main__':
    with open('BasicGraph.json') as json_file:
        json_user = json.load(json_file)
    account = parse_user(json_user)
    # print(account)
    filter_network("", account)
