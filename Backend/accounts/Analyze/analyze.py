import networkx as nx
import matplotlib

matplotlib.use('Agg')
from matplotlib import pyplot as plt
from pyvis.network import Network

from ..modules.Account import Account
from ..modules.Ego.Colleague import Colleague
from ..modules.Ego.CoStudent import CoStudent
from ..modules.Ego.Neighbors import Neighbors
from ..modules.Ego.ChildhoodFriend import ChildhoodFriend
from ..modules.Ego.Family import Family
from ..modules.Threshold import ConnectionThreshold, Threshold, UserThreshold

module_map = {"family": Family(), "colleague": Colleague(), "co_students": CoStudent(),
              "neighbors": Neighbors(), "childhood_friends": ChildhoodFriend()}


def filter_network(thresholds, account):
    filter_ego_attributes(account.connection.attributes)
    mutual_friends = int(thresholds['mutual_friends'])
    action = str(thresholds['selected_action'])
    friendship_duration = int(thresholds['friendship_duration'])
    total_friends = int(thresholds['total_friends'])
    age_of_account = int(thresholds['age_of_account'])

    # Debugging
    # mutual_friends = 10
    # action = "Sharing"
    # friendship_duration = 365
    # total_friends = 355
    # age_of_account = 365

    set_threshold(Threshold(ConnectionThreshold(mutual_friends, friendship_duration, account.connection.attributes),
                            UserThreshold(total_friends, age_of_account)), account)
    G = init_graph(account, action, float(thresholds["minimum_trust_value"]))
    # G = init_graph(account, "Sharing", 0)

    G2 = Network("500px", "1000px")
    G2.from_nx(G)
    G2.show(account.name + ".html")
    G.clear()
    plt.close()


def set_threshold(thresholds: Threshold, account):
    for field in account.friends:
        for member in account.friends[field]:
            member.set_trust_value(thresholds)
            set_threshold(thresholds, member)


def filter_ego_attributes(attributes):
    for field in attributes:
        attribute_arr = attributes[field].split('\n')
        for i in range(len(attribute_arr)):
            attribute_arr[i] = attribute_arr[i].replace("Works at ", "")
            attribute_arr[i] = attribute_arr[i].replace("Worked at ", "")
            attribute_arr[i] = attribute_arr[i].replace("Went to ", "")
            attribute_arr[i] = attribute_arr[i].replace("From ", "")
            attribute_arr[i] = attribute_arr[i].replace("Studied at ", "")
            attribute_arr[i] = attribute_arr[i].replace("Lives in ", "")
            attribute_arr[i] = attribute_arr[i].replace("Past: ", "")
        attributes[field] = attribute_arr


def add_subgraph(account: Account, graph, action, minimum_trust_value, connection_degree):
    for field in account.friends:
        print(action)
        if connection_degree == 0:
            permission = module_map[field].is_permissioned(action)
            print("Permission is:" + str(permission) + " to field " + field)
        else:
            permission = action
        if permission:
            color = "green"
            follow_up_action = True
        else:
            color = "red"
            follow_up_action = False
        for member in account.friends[field]:
            account_trust_value = member.account_trust_value
            if account_trust_value < minimum_trust_value and color != "red":
                color = "black"
            node_title = member.name + " UTV: " + str(member.account_trust_value) \
                         + '\nAOA: ' + str(member.user.age_of_account) + '\nTF: ' \
                         + str(member.user.total_friends)
            edge_title = member.name + \
                         " MF: " + str(member.connection.mutual_friends) + \
                         " FD: " + str(member.connection.friendship_duration)
            graph.add_node(member.name, title = node_title)
            graph.add_edge(account.name, member.name, title = edge_title, value = 2, color = color)

            # graph.add_node(member.name, title = "node_title")
            # graph.add_edge(account.name, member.name, title = "edge_title", value = 2, color = color)

            add_subgraph(member, graph, follow_up_action, minimum_trust_value, connection_degree + 1)


def init_graph(account = None, action = None, minimum_trust_value: float = 0):
    G = nx.Graph()
    print(action)
    G.add_node(account.name, value = 20, color = "black")
    add_subgraph(account, G, action, minimum_trust_value, connection_degree = 0)
    return G
