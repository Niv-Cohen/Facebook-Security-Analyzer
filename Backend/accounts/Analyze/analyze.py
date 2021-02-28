import networkx as nx
import matplotlib
matplotlib.use ('Agg')
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

    G2 = Network("500px", "1000px")
    G2.from_nx(G)
    # G2.save_graph()
    G2.show(account.name+".html")
    # nx.draw(G, with_labels = True, font_size=12, font_family="times new roman", bbox=dict(facecolor="red", alpha=.5))
    # plt.savefig("../client/src/assets/"+account.name+".png")

    # plt.savefig("./" + account.name + ".png")
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


def add_subgraph(account: Account, graph, action = None, minimum_trust_value:float = 0, connection_degree:int = 1):
    for field in account.friends:
        permission = True if module_map[field].is_permissioned(action) or action is None else False
        if permission:
            for member in account.friends[field]:
                account_trust_value = member.account_trust_value
                if account_trust_value > minimum_trust_value:
                    graph.add_node(member.name.split()[0])
                    graph.add_edge(account.name.split()[0], member.name.split()[0])
                    add_subgraph(member, graph)


def init_graph(account=None, action = None, minimum_trust_value: float = 0):
    G = nx.Graph()
    G.add_node(account.name.split()[0], value=15, color="black")
    add_subgraph(account, G, action, minimum_trust_value)
    return G










