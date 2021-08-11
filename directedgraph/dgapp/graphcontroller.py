import sys
from pathlib import Path

print("Running" if __name__ == "__main__" else "Importing", Path(__file__).resolve())
CURRENT_DIRECTORY = Path(__file__).absolute()
ROOT_FOLDER = CURRENT_DIRECTORY.parent.parent.parent
sys.path.append(str(ROOT_FOLDER))

from directedgraph.dgcore import GroundNode


class GraphController:
    # dictionary for the number of ground and source nodes
    # node_counter = {
    #     "GroundNode": 0,
    #     "SourceNode": 0,
    # }
    # dictionary that uses the node IDs as keys and the number of arcs it is connected to as value pair
    # arc_counter = {}
    # a = 0
    # b = 0

    def __init__(self):
        self.node_counter = {
            "GroundNode": 0,
            "SourceNode": 0,
        }
        self.arc_counter = {}
        self.a = 0
        self.b = 0

    def add_ground_node(self):
        # self.a = self.a + 1
        # self.node_counter["GroundNode"] = self.a
        self.node_counter["GroundNode"] = self.node_counter["GroundNode"] + 1

    def remove_ground_node(self):
        # self.a = self.a - 1
        # self.node_counter["GroundNode"] = self.a
        self.node_counter["GroundNode"] = self.node_counter["GroundNode"] - 1

    def add_source_node(self):
        self.b = self.b + 1
        self.node_counter["SourceNode"] = self.b

    def remove_source_node(self):
        self.b = self.b - 1
        self.node_counter["SourceNode"] = self.b

    def add_arc(self, node1, node2):
        if node1 in self.arc_counter:
            self.arc_counter[node1] = self.arc_counter[node1] + 1

        else:
            self.arc_counter[node1] = 1

        if node2 in self.arc_counter:
            self.arc_counter[node2] = self.arc_counter[node2] + 1

        else:
            self.arc_counter[node2] = 1

    def remove_arc(self, node1, node2):
        self.arc_counter[node1] = self.arc_counter[node1] - 1
        self.arc_counter[node2] = self.arc_counter[node2] - 1

    def create_component(self, graph_instance, parameters):
        if parameters["type"] == "GroundNode":
            if self.node_counter["GroundNode"] == 0:
                temp = graph_instance.create_component(parameters)
                self.add_ground_node()
                return temp
            else:
                return "Ground Node already exist"

        if parameters["type"] == "SourceNode":
            temp = graph_instance.create_component(parameters)
            self.add_source_node()
            return temp

        if parameters["type"] == "Node":
            temp = graph_instance.create_component(parameters)
            return temp

        if parameters["type"] == "Arc":

            if parameters["node1"] == "SourceNode":
                if (
                    parameters["node1_uid"] in self.arc_counter
                ):  # if it exist in the arc_counter, there is already 1 arc connected to source node
                    return "Source nodes can only have one arc"
                else:
                    valid1 = 1  # source node does not have an arc yet

            else:
                if (
                    parameters["node1_uid"] in self.arc_counter
                ):  # if they have at least 1 arc
                    if (
                        self.arc_counter[parameters["node1_uid"]] > 49
                    ):  # for any node it cannot have more than 50 arcs.
                        return "Each node cannot have more than 5 arcs"
                    else:
                        valid1 = 1

                else:  # if they have no arcs yet
                    valid1 = 1  # Valid 1 will be true if the node of a specific type is not connected to too many arcs

            if parameters["node2"] == "SourceNode":
                if parameters["node2_uid"] in self.arc_counter:
                    return "Source nodes can only have one arc"
                else:
                    valid2 = 1

            else:
                if parameters["node2_uid"] in self.arc_counter:
                    if self.arc_counter[parameters["node2_uid"]]:
                        return "Each node cannot have more than 50 arcs"
                    else:
                        valid2 = 1

                else:
                    valid2 = 1  # Valid 2 is the same as Valid one but it is for the checking of second node

            if (
                parameters["user_defined_attribute"] > 0
            ):  # arc properties cannot be negative
                valid3 = 1
            else:
                return "Arc Property Must be Positive"

            if (valid1 == 1) and (valid2 == 1) and (valid3 == 1):
                temp = graph_instance.create_component(
                    parameters
                )  # if it passes the tests, the arc will be created
                self.add_arc(
                    parameters["node1_uid"], parameters["node2_uid"]
                )  # pass the 2 node IDs to be used as keys in the arc_counter dictionary
                return temp

    def delete_component(self, graph_instance, uid):
        # if parameters["type"] == "SourceNode":
        #     if self.node_counter["SourceNode"] == 1:
        #         return "There must be at least one source node"
        #     else:
        #         temp = graph_instance.delete_component(parameters["uid"])
        #         self.remove_source_node()
        #         return temp

        # if parameters["type"] == "GroundNode":
        #     if self.node_counter["GroundNode"] == 1:
        #         return "There must be at least one ground node"
        #     else:
        #         temp = graph_instance.delete_component(parameters["uid"])
        #         self.remove_ground_node()
        #         return temp

        # if parameters["type"] == "Node":
        #     temp = graph_instance.delete_component(parameters["uid"])
        #     return temp

        # if parameters["type"] == "Arc":
        #     temp = graph_instance.delete_component(parameters["uid"])
        #     self.remove_arc(parameters["node1_uid"], parameters["node2_uid"])

        component_type = type(graph_instance.get_component(uid))

        if component_type == GroundNode:
            return "There must be at least one ground node"
        else:
            temp = graph_instance.delete_component(uid)
            return temp
