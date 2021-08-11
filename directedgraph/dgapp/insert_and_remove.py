import sys
from pathlib import Path

print("Running" if __name__ == "__main__" else "Importing", Path(__file__).resolve())
CURRENT_DIRECTORY = Path(__file__).absolute()
ROOT_FOLDER = CURRENT_DIRECTORY.parent.parent.parent
sys.path.append(str(ROOT_FOLDER))

from directedgraph.dgcore import (
    Node,
    SourceNode,
    GroundNode,
    Arc,
)  # import the right classes from dgcore. Not sure if these are correct


class Counter:
    node_counter = {"GroundNode": 0, "SourceNode": 0}
    arc_counter = {}
    a = 0
    b = 0

    def __init__(self, node_counter, arc_counter, a, b):
        self.node_counter = node_counter
        self.arc_counter = arc_counter
        self.a = a
        self.b = b

    def add_ground_node(self):
        self.a = self.a + 1
        self.node_counter["GroundNode"] = self.a

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


class Insert_Remove_Component(Counter):
    def __init__(self, position_x, position_y, colour, NodeName, ArcName, value):
        self = Counter
        self.position_x = position_x
        self.position_y = position_y
        self.colour = colour
        self.NodeName = NodeName
        self.ArcName = ArcName
        self.value = value

    def insert_ground_node(self, position_x, position_y, colour, NodeName):
        if self.node_counter["GroundNode"] == 0:
            id = generate_uid
            create_component(
                {
                    "type": "GroundNode",
                    "name": NodeName,
                    "uid": id,
                    "colour": colour,
                    "position_x": position_x,
                    "position_y": position_y,
                }
            )
            self.add_ground_node()
            return id
        else:
            return "Ground Node already exist"

    def insert_source_node(self, position_x, position_y, colour, NodeName, value):
        id = generate_uid
        create_component(
            {
                "type": "SourceNode",
                "name": NodeName,
                "uid": id,
                "colour": colour,
                "position_x": position_x,
                "position_y": position_y,
                "user_defined_attribute": value,
            }
        )
        self.add_source_node()
        return id

    def insert_node(self, position_x, position_y, colour, NodeName):
        id = generate_uid
        create_component(
            {
                "type": "SourceNode",
                "name": NodeName,
                "uid": id,
                "colour": colour,
                "position_x": position_x,
                "position_y": position_y,
            }
        )
        return id

    def insert_arc(self, node1, node2, type1, type2, value, colour, ArcName):
        if type1 == "SourceNode":
            if (
                node1 in self.arc_counter
            ):  # if it exist in the arc_counter, there is already 1 arc connected to source node
                return "Source nodes can only have one arc"
            else:
                valid1 = 1  # source node does not have an arc yet
        else:
            if node1 in self.arc_counter:  # if they have at least 1 arc
                if (
                    self.arc_counter[node1] > 49
                ):  # for any node it cannot have more than 50 arcs.
                    return "Each node cannot have more than 5 arcs"
                else:
                    valid1 = 1

            else:  # if they have no arcs yet
                valid1 = 1

        if type2 == "SourceNode":
            if (
                node2 in self.arc_counter
            ):  # if it exist in the arc_counter, there is already 1 arc connected to source node
                return "Source nodes can only have one arc"
            else:
                valid2 = 1  # source node does not have an arc yet
        else:
            if node2 in self.arc_counter:  # if they have at least 1 arc
                if (
                    self.arc_counter[node2] > 4
                ):  # for any node it cannot have more than 50 arcs. For testing, it cannot have more than 5.
                    return "Each node cannot have more than 5 arcs"
                else:
                    valid2 = 1

            else:  # if they have no arcs yet
                valid2 = 1

        if value > 0:
            valid3 = 1
        else:
            return "Arc Property Must be Positive"

        if (valid1 == 1) and (valid2 == 1) and (valid3 == 1):
            id = generate_uid
            create_component(
                {
                    "type": "Arc",
                    "name": ArcName,
                    "uid": id,
                    "colour": colour,
                    "node1_uid": node1,
                    "node2_uid": node2,
                }
            )
            self.add_arc(node1, node2)

    def delete_node(self, type, nodeid):
        if type == "SourceNode":
            if self.node_counter["SourceNode"] == 1:
                return "There must be at least one source node"
            else:
                delete_component(nodeid)
                self.remove_source_node()
        elif type == "Node":
            delete_component(nodeid)
        else:
            return "error"

    def delete_arc(self, arcid, node1, node2):
        delete_component(arcid)
        self.remove_arc(node1, node2)
